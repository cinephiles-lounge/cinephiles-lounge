import requests
from django.conf import settings
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import *
from .serializers import *
from datetime import date



tmdb_api_key = settings.TMDB_API_KEY
tmdb_access_token = settings.TMDB_ACCESS_TOKEN

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {tmdb_access_token}"
}



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
        


# 영화 DB 저장 함수
def save_movies(result_arr):
    for movie_data in result_arr:
    # 현재 영화가 이미 DB에 저장되어 있다면 변동 가능성 있는 popularity, vote_average, vote_count를 업데이트 후 수정
        if Movie.objects.filter(movie_id=movie_data.get('id')).exists():
            movie = Movie.objects.get(movie_id=movie_data.get('id'))
            movie.popularity = movie_data.get('popularity')
            movie.vote_average = movie_data.get('vote_average')
            movie.vote_count = movie_data.get('vote_count')
            movie.save()
        # 현재 영화가 DB에 저장되어있지 않은 새 영화라면 인스턴스 생성 후 저장
        else:
            new_movie = Movie()
            new_movie.movie_id = movie_data.get('id')
            new_movie.title = movie_data.get('title')
            new_movie.overview = movie_data.get('overview')
            new_movie.popularity = movie_data.get('popularity')
            new_movie.release_date = movie_data.get('release_date')
            new_movie.vote_average = movie_data.get('vote_average')
            new_movie.vote_count = movie_data.get('vote_count')
            new_movie.poster_path = movie_data.get('poster_path')
            new_movie.trailer_key = get_trailer_key(new_movie.movie_id)
            new_movie.save()
            
            genres = movie_data.get('genre_ids')

            for genre_id in genres:
                genre = Genre.objects.get(genre_id=genre_id)
                new_movie.genres.add(genre)



# 트레일러 youtube video key를 반환하는 함수
def get_trailer_key(movie_id):
    languages = ['ko-KR', 'en-US']
    trailer_key = ''

    # 한국어 검색 결과가 나오지 않으면 영어로도 검색
    for language in languages:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}/videos?language={language}'
        videos = requests.get(url, headers=headers).json().get('results')

        # 해당 영화의 비디오 검색 결과가 존재하면
        if videos:
            # 비디오들이 담긴 배열을 순회                
            for video in videos:
                if video.get('type') == 'Trailer':
                    trailer_key = video.get('key')
                    return trailer_key
    
    return trailer_key