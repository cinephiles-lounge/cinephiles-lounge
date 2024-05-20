import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ..models import *
from soynlp.word import WordExtractor
from soynlp.noun import LRNounExtractor_v2
from soynlp.tokenizer import LTokenizer
from .stop_words import stop_words

def clean_string(text):
    tokens = ''
    for char in text:
        tokens += char + ' '
    return tokens

def search(keyword):
    # 영화 정보를 Pandas 데이터프레임으로 변환
    movies = Movie.objects.all()

    movies_df_1 = pd.DataFrame(data=[keyword], columns=['title'])
    movies_df_2 = pd.DataFrame(Movie.objects.values('title'))
    movies_df = pd.concat([movies_df_1, movies_df_2], ignore_index=True)
    movies_df['title'] = movies_df['title'].apply(clean_string)
    movies_df['title'] = movies_df['title'].apply(clean_string)
    # print(movies_df)
    corpus = [keyword]
    for movie in Movie.objects.values('title'):
        corpus.append(movie.get('title'))

    print(corpus)
    word_extractor = WordExtractor(corpus)
    words = word_extractor.extract()
    print(words)

    noun_extractor = LRNounExtractor_v2(verbose=True)
    nouns = noun_extractor.train_extract(corpus)
    tokenizer = LTokenizer(scores=nouns)

    count_vect = CountVectorizer(tokenizer=tokenizer.tokenize, stop_words=stop_words)
    count_matrix = count_vect.fit_transform(corpus)
    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    sim_scores = list(enumerate(cosine_sim[0]))
    sim_scores = sorted(sim_scores, key=lambda tpl: tpl[1], reverse=True)
    print(sim_scores)
    sim_scores = sim_scores[1:11]


    movie_indices = [tpl[0] for tpl in sim_scores]
    # print(movies_df.iloc[[movie_indices[0]]])
    # print(movie_indices)

    return movie_indices

