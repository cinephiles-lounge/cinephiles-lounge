import pandas as pd
import re
from sklearn.metrics.pairwise import cosine_similarity
from ..models import *
from soynlp.tokenizer import LTokenizer
from soynlp.word import WordExtractor
from soynlp.vectorizer import sent_to_word_contexts_matrix
from scipy.sparse import csr_matrix

def clean_string(text):
    cleaned_text = re.sub(r'[^a-zA-Z가-힣0-9\s]', '', text)
    return cleaned_text

def tokenize(text):
    tokenizer = LTokenizer()
    tokens = tokenizer.tokenize(text)
    return tokens

def train_soynlp_word_vectorizer(tokenized_titles):
    word_extractor = WordExtractor()
    word_extractor.train(tokenized_titles)
    word_scores = word_extractor.extract()
    word_scores = {word: score.cohesion_forward for word, score in word_scores.items()}
    word_vectorizer = sent_to_word_contexts_matrix(tokenized_titles, windows=3, min_tf=2,
                                                   dynamic_weight=True, verbose=True)
    return word_vectorizer

def search(keyword):
    # 영화 정보를 Pandas 데이터프레임으로 변환
    movies = Movie.objects.all()

    movies_df = pd.DataFrame(Movie.objects.values('title'))
    movies_df['title'] = movies_df['title'].apply(clean_string)

    # Soynlp로 토큰화하기
    movies_df['tokens'] = movies_df['title'].apply(tokenize)

    # 키워드 토큰화
    keyword_tokens = tokenize(keyword)
    print(keyword_tokens)

    # 각 영화 제목에 대한 토큰화된 문장을 하나의 문자열로 변환
    tokenized_titles = [' '.join(tokens) for tokens in movies_df['tokens']]

    # Soynlp로 word vectorizer 학습
    word_vectorizer = train_soynlp_word_vectorizer(tokenized_titles)

    # 키워드에 대한 word vectorizer 생성
    keyword_indices = [word_vectorizer[0].index(token) for token in word_vectorizer[0] if token in keyword_tokens]
    keyword_vector = word_vectorizer[:, keyword_indices]

    # 희소 행렬로 변환
    keyword_vector = csr_matrix(keyword_vector)

    # 각 영화와의 코사인 유사도 계산
    cosine_sim = cosine_similarity(keyword_vector, word_vectorizer)

    # 유사도가 높은 영화 인덱스 추출
    sim_scores = list(enumerate(cosine_sim[0]))
    sim_scores = sorted(sim_scores, key=lambda tpl: tpl[1], reverse=True)
    sim_scores = sim_scores[1:11]  # 자기 자신은 제외

    movie_indices = [tpl[0] for tpl in sim_scores]

    return movie_indices