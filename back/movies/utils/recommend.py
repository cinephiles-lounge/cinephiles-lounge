import pandas as pd
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random

# Function to convert all strings to lower case and strip names of spaces
def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        #Check if director exists. If not, return empty string
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''


# Credits, Genres and Keywords based recommender
df = pd.read_csv('./tmdb_5000_movies.csv')
print(df.info())
features = ['overview', 'genres']
    
for feature in features:
    df[feature] = df[feature].apply(literal_eval)
    df[feature] = df[feature].apply(lambda arr : [dict['name'] for dict in arr])
    df[feature] = df[feature].apply(clean_data)

def create_soup(x):
    return ' '.join(x['production_countries']) + ' ' + ' '.join(x['keywords']) + ' ' + ' '.join(x['genres'])

df['soup'] = df.apply(create_soup, axis=1)
print(df['soup'])

count_vect = CountVectorizer(stop_words='english',min_df=0.0,ngram_range=(1,2))
count_matrix = count_vect.fit_transform(df['soup'])
cosine_sim = cosine_similarity(count_matrix, count_matrix)

indices = pd.Series(df.index, index=df['title']).drop_duplicates()

def get_recommendations(movie_titles, cosine_sim=cosine_sim):
    recommended_movies = pd.DataFrame()
    for title in movie_titles:
        idx = indices[title]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]
        movie_indices = [x[0] for x in sim_scores]
        recommended_movies = pd.concat([recommended_movies, df['title'].iloc[movie_indices]]).drop_duplicates()
    return recommended_movies.sample(n=10)

print(get_recommendations(['The Dark Knight Rises']))