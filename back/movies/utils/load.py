import requests
from ..models import *

# 영화 DB 저장 함수
def save_movies(result_arr):
    did_create = False
    processed = 0

    # 줄거리, 트레일러 없으면 저장 안되게
    for movie_data in result_arr:
    # 현재 영화가 이미 DB에 저장되어 있다면 변동 가능성 있는 popularity, vote_average, vote_count를 업데이트 후 수정
        if Movie.objects.filter(movie_id=movie_data.get('id')).exists():
            movie = Movie.objects.get(movie_id=movie_data.get('id'))
            movie.popularity = movie_data.get('popularity')
            movie.vote_average = movie_data.get('vote_average')
            movie.vote_count = movie_data.get('vote_count')
            movie.save()
            processed += 1
        # 현재 영화가 DB에 저장되어있지 않은 새 영화라면 인스턴스 생성 후 저장
        else:
            new_movie = Movie()

            overview = movie_data.get('overview')
            if not overview:
                continue

            trailer_key = get_trailer_key(movie_data.get('id'))
            if not trailer_key:
                continue
            
            new_movie.overview = overview
            new_movie.trailer_key = trailer_key

            new_movie.movie_id = movie_data.get('id')
            new_movie.is_adult = movie_data.get('adult')
            new_movie.title = movie_data.get('title')
            new_movie.popularity = movie_data.get('popularity')
            new_movie.release_date = movie_data.get('release_date')
            new_movie.vote_average = movie_data.get('vote_average')
            new_movie.vote_count = movie_data.get('vote_count')
            new_movie.poster_path = movie_data.get('poster_path')
            new_movie.backdrop_path = movie_data.get('backdrop_path')

            new_movie.save()

            did_create = True
            processed += 1

            genres = movie_data.get('genre_ids')

            for genre_id in genres:
                genre = Genre.objects.get(genre_id=genre_id)
                new_movie.genres.add(genre)

    return (did_create, processed)
        

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


tmdb_api_key = settings.TMDB_API_KEY
tmdb_access_token = settings.TMDB_ACCESS_TOKEN

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {tmdb_access_token}"
}