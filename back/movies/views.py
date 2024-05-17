import requests
from django.conf import settings
from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import *
from .serializers import *
from datetime import date
from .utils.load import save_movies, headers
from .utils.recommend import recommend



# 전체 영화 조회
@api_view(['GET'])
def get_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



# 현재 상영작 조회 (3위까지)
@api_view(['GET'])
def get_playing(request):
    if request.method == 'GET':
        url = 'https://api.themoviedb.org/3/movie/now_playing?language=ko-KR&page=1'
        now_playing_movies = requests.get(url, headers=headers).json().get('results')
        save_movies(now_playing_movies)

        top3_ids = []
        for i in range(3):
            top3_ids.append(now_playing_movies[i].get('id'))

        top3_movies = Movie.objects.filter(movie_id__in=top3_ids)
        serializer = MovieSerializer(top3_movies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



# 상영 예정작 20개 조회
@api_view(['GET'])
def get_upcoming(request):
    if request.method == 'GET':
        url = f"https://api.themoviedb.org/3/discover/movie?language=ko-KR&page=1&sort_by=popularity.desc&primary_release_date.gte={date.today()}"
        upcoming_movies = requests.get(url, headers=headers).json().get('results')
        print(url)
        save_movies(upcoming_movies)

        ids = []

        for i in range(20):
            ids.append(upcoming_movies[i].get('id'))

        upcoming_movies = Movie.objects.filter(movie_id__in=ids)
        serializer = MovieSerializer(upcoming_movies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



# 한 페이지 당 영화 20개씩 리턴
# 초당 요청 max: around 50
@api_view(['POST'])
def set_db(request):
    if request.method == 'POST':

        # 1~50 페이지 요청 == 1000개 영화 저장
        for i in range(1, 51):
            url = f'https://api.themoviedb.org/3/movie/popular?language=ko-KR&page={i}'
            response = requests.get(url, headers=headers).json()
            save_movies(response.get('results'))

        return Response(status=status.HTTP_200_OK)



# 장르 정보 불러오기
# DB에 장르 데이터가 없을때만 저장함
@api_view(['POST'])
def get_genre(request):
    if request.method == 'POST':
        if not Genre.objects.filter(id=1).exists():
            url = 'https://api.themoviedb.org/3/genre/movie/list?language=ko'
            response = requests.get(url, headers=headers).json()
            
            for genre in response.get('genres'):
                data = {
                    'genre_id': genre.get('id'),
                    'name': genre.get('name')
                }
                
                serializer = GenreSerializer(data=data)

                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    
            return Response(status=status.HTTP_201_CREATED)
        else:
            message = {
                'message': '장르 데이터가 이미 존재합니다.'
            }
            return Response(data=message)



# 영화 상세 조회
@api_view(['GET'])
def get_movie_detail(request, movie_pk):
    if request.method == 'GET':
        movie = Movie.objects.get(pk=movie_pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)



# 영화 좋아요
@api_view(['POST'])
def movie_like(request, movie_pk):
    if request.method == 'POST':
        movie = Movie.objects.get(pk=movie_pk)
        
        if movie.like_users.filter(pk=request.user.pk).exists():
            movie.liked_users.remove(request.user)
        else:
            movie.liked_users.add(request.user)
        
        data = {
            'like_count': movie.like_users.count()
        }
        return Response(data, status=status.HTTP_200_OK)
        
        


# 미완성
@api_view(['GET'])
def get_recommendation_like(request):
    recommend()
    return Response({'실행': 'O'})