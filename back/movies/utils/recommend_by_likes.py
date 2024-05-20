import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ..models import *


def clean_string(text):
    cleaned_text = re.sub(r'[^a-zA-Z가-힣0-9\s]', '', text)
    return cleaned_text

def recommend_by_likes(liked_movies):

    # 영화 데이터를 genre M:N 필드와 함께 불러옴
    movies = Movie.objects.all().prefetch_related('genres')

    # 영화 정보를 Pandas 데이터프레임으로 변환
    movie_data = []
    for movie in movies:
        genres = ' '.join([genre.name for genre in movie.genres.all()])
        movie_data.append({
            'movie_id': movie.movie_id, 
            'title': movie.title, 
            'genres': genres
        })

    movies_df = pd.DataFrame(movie_data)
    movies_df.index = movies_df.index + 1

    # 영화 제목은 특수문자를 제거 후 사용
    # soup은 영화 제목과 장르를 공백 단위로 이어놓은 Meta Data를 담은 스트링
    movies_df['title'] = movies_df['title'].apply(clean_string)
    movies_df['soup'] = movies_df['title'] + ' ' + movies_df['genres']

    # CountVectorizer와 TF-IDF(Term Frequency-Inverse Document Frequency)는 둘 다 자연어 처리에서 텍스트 데이터를 수치화하는 데 사용되는 방법
    # TF-IDF는 모든 문서에 공통적으로 나타나는 단어의 중요도를 감소시키므로 여기서는 사용하지 않음
    # 단순히 단어의 출현 빈도만 고려하기 위해 CountVectorizer 사용
    count_vect = CountVectorizer()

    # 주어진 문서 집합에 대해 어휘 사전을 구축(fit)하고 문서를 벡터로 변환(transform)하여 희소 행렬로 반환
    # 그냥 행렬로 처리하면 0이 너무 많아져서 메모리 낭비
    # fit: 각 단어의 인덱스를 매핑
    # transform: 각 문서를 어휘 사전에 등장하는 단어의 출현 빈도로 표현하여 벡터 형태로 반환
    count_matrix = count_vect.fit_transform(movies_df['soup'])

    # 코사인 유사도: 벡터의 길이에 영향을 받지 않고 오직 방향으로만 유사도를 판단 (x벡터와 y벡터가 이루는 각의 코사인 값)
    # 각각의 벡터의 길이(단어의 수)에 가중치를 두지 않고 단순히 단어간의 조합이 비슷함을 판단해야 하므로 코사인 유사도를 사용
    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    # 좋아요 한 영화를 순회하며 각 영화와 비슷한 10개의 영화를 recommended_movies에 넣어줌
    recommended_movies = set()

    # 유저가 좋아요 한 영화가 N개: len(recommended_movies) = N * 10
    for movie in liked_movies:

        # 해당 영화와 전체 영화의 코사인 유사도를 담은 행을 가져옴
        sim_scores = list(enumerate(cosine_sim[movie.id - 1]))

        # 해당 행을 코사인 유사도(x[1])를 기준으로 내림차순으로 정렬함
        # tpl == tuple == (idx, cos_sim)
        sim_scores = sorted(sim_scores, key=lambda tpl: tpl[1], reverse=True)

        # 자기 자신을 제외하고 자기 자신과 가장 비슷한 10개의 영화
        sim_scores = sim_scores[1:11]

        # 중복을 방지하기 위해 set로 넣어줌
        movie_indices = [tpl[0] for tpl in sim_scores]
        for idx in movie_indices: 
            recommended_movies.add(idx + 1)

    return recommended_movies


"""
참고1:
https://www.kaggle.com/code/ibtesama/getting-started-with-a-movie-recommendation-system

참고2:
https://m.blog.naver.com/PostView.naver?blogId=myincizor&logNo=221643594756&fromRecommendationType=category

참고3:
코사인 유사도

코사인 유사도를 이해하는 한 가지 방법은 벡터의 방향이 중요한 상황에서 어떻게 유용한지를 생각해보는 것입니다. 
여기에 간단한 예시를 들어볼게요.

상상해보세요, 당신이 한국어와 영어 두 가지 언어로 된 단어 벡터를 가지고 있다고 합시다. 
벡터의 각 차원은 각각 한국어와 영어에서의 단어의 출현 빈도를 나타냅니다. 
이제 다음 두 단어 벡터를 비교해봅시다.

한국어: [3, 1], 영어: [1, 3]
한국어: [2, 2], 영어: [2, 2]

두 번째 예에서는 어떤 언어에서든 단어의 출현 빈도가 동일합니다. 
이 두 벡터는 길이(크기)가 같습니다. 
그러나 첫 번째 예에서는 각각의 언어에서의 단어의 출현 빈도가 다릅니다. 
이 경우, 벡터의 크기가 중요하지 않고 벡터의 방향(즉, 각 언어에서의 단어 빈도의 상대적인 비율)이 중요합니다.

코사인 유사도는 벡터의 크기가 아니라 벡터의 방향을 고려하여 두 벡터 간의 유사성을 측정합니다. 
따라서 첫 번째 예에서는 두 벡터가 서로 다른 크기를 가지고 있더라도, 코사인 유사도를 계산할 때, 
각 언어에서의 단어 빈도의 상대적인 비율을 고려하여 벡터 간의 유사성을 측정합니다. 
이것이 바로 벡터의 크기가 중요하지 않고 방향이 중요한 상황에서 코사인 유사도가 유용하게 사용되는 이유입니다.
"""