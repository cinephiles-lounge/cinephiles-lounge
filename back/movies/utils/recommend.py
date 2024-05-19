import pandas as pd
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ..models import *
import random
import re

def clean_string(text):
    cleaned_text = re.sub(r'[^a-zA-Z가-힣0-9\s]', '', text)
    return cleaned_text


# https://www.kaggle.com/code/ibtesama/getting-started-with-a-movie-recommendation-system
def recommend(liked_movies):
    movies = Movie.objects.all().prefetch_related('genres')

    # 영화 정보를 Pandas 데이터프레임으로 변환
    movie_data = []
    for movie in movies:
        genres = ' '.join([genre.name for genre in movie.genres.all()])
        movie_data.append({'movie_id': movie.movie_id, 'title': movie.title, 'genres': genres})
    movies_df = pd.DataFrame(movie_data)
    movies_df.index = movies_df.index + 1
    movies_df['title'] = movies_df['title'].apply(clean_string)
    movies_df['soup'] = movies_df['title'] + ' ' + movies_df['genres']
    # print(movies_df['soup'])

    count_vect = CountVectorizer()
    count_matrix = count_vect.fit_transform(movies_df['soup'])
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    recommended_movies = set()

    for movie in liked_movies:
        # print('----------')
        # print(movies_df.iloc[[movie.id-1]])
        sim_scores = list(enumerate(cosine_sim[movie.id - 1]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]
        movie_indices = [x[0] for x in sim_scores]
        for idx in movie_indices: 
            recommended_movies.add(idx + 1)
            # print(movies_df.iloc[[idx]])
        # print('---------')

    return recommended_movies
