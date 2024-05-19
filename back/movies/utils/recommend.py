import pandas as pd
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
from ..models import *


def create_soup(arr):
    return ' '.join(arr)

# https://www.kaggle.com/code/ibtesama/getting-started-with-a-movie-recommendation-system
def recommend(genres):

    movies = Movie.objects.all()
    df = pd.DataFrame(list(movies.values()))

    qs = Movie.objects.prefetch_related('genres')

    # genre_df = pd.DataFrame(columns=['genre'])
    # for q in qs:
    # df1 = pd.DataFrame(list(qs.values()))
    # print(df1['genres'])

    # df['genres'] = df['genres'].apply(literal_eval)

    # print(df['genres'])

    # df['soup'] = df['overview'].apply(create_soup)

    # print(df['soup'])

    count_vect = CountVectorizer()
    # count_matrix = count_vect.fit_transform(df['soup'])
    # cosine_sim = cosine_similarity(count_matrix, count_matrix)

    # indices = pd.Series(df.index, index=df['title']).drop_duplicates()

    # recommended_movies = pd.DataFrame()

    # for title in movie_titles:
    #     idx = indices[title]
    #     sim_scores = list(enumerate(cosine_sim[idx]))
    #     sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    #     sim_scores = sim_scores[1:11]
    #     movie_indices = [x[0] for x in sim_scores]
    #     recommended_movies = pd.concat([recommended_movies, df['title'].iloc[movie_indices]]).drop_duplicates()

    # return recommended_movies.sample(n=10)