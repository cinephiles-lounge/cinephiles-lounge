import requests
from django.conf import settings
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import *
from .serializers import *


tmdb_api_key = settings.TMDB_API_KEY
tmdb_access_token = settings.TMDB_ACCESS_TOKEN

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {tmdb_access_token}"
}

def get_trailer_key(movie_id):
    languages = ['ko-KR', 'en-US']
    trailer_key = ''

    # 한국어 검색 결과가 나오지 않으면 영어로도 검색
    for language in languages:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}/videos?language={language}'
        videos = requests.get(url, headers=headers).json().get('results')
        print(videos)

        # 해당 영화의 비디오 검색 결과가 존재하면
        if videos:
            # 비디오들이 담긴 배열을 순회                
            for video in videos:
                if video.get('type') == 'Trailer':
                    trailer_key = video.get('key')
                    return trailer_key
    
    return trailer_key



# 한 페이지 당 영화 20개씩 리턴
# 초당 요청 max: around 50
@api_view(['POST'])
def set_db(request):
    if request.method == 'POST':

        for i in range(1, 31):
            url = f'https://api.themoviedb.org/3/movie/popular?language=ko-KR&page={i}'
            response = requests.get(url, headers=headers).json()
            
            for movie_data in response.get('results'):
                if Movie.objects.filter(movie_id=movie_data.get('id')).exists():
                    print('exist')
                    movie = Movie.objects.get(movie_id=movie_data.get('id'))
                    movie.popularity = movie_data.get('popularity')
                    movie.vote_average = movie_data.get('vote_average')
                    movie.vote_count = movie_data.get('vote_count')
                    movie.save()
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
                
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def get_genre(request):
    if request.method == 'POST':
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