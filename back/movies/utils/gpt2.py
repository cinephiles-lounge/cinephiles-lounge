    # movies = Movie.objects.all().prefetch_related('genres')

    # # 영화 정보를 Pandas 데이터프레임으로 변환
    # movie_data = []
    # for movie in movies:
    #     genres = ', '.join([genre.name for genre in movie.genres.all()])
    #     movie_data.append({'id': movie.movie_id, 'title': movie.title, 'overview': movie.overview, 'genres': genres})
    # movies_df = pd.DataFrame(movie_data)

    # print(movies_df)
    
    # movies_df['soup'] = movies_df['title'] + ' ' + movies_df['overview'] + ' ' + movies_df['genres']

    # # KoGPT2 tokenizer 및 model 초기화
    # tokenizer = GPT2Tokenizer.from_pretrained("skt/kogpt2-base-v2")
    # model = GPT2Model.from_pretrained("skt/kogpt2-base-v2")

    # # KoGPT2를 사용하여 임베딩 벡터 생성
    # embeddings = []
    # for text in movies_df['description']:
    #     """
    #     그래디언트는 함수의 기울기를 나타내는 벡터로 딥러닝에서는 일반적으로 손실 함수를 최소화하는 방향으로 모델의 가중치를 조정해 나갈 때 사용
    #     모델 학습, 모델 평가 등 모델의 파라미터를 업데이터해야 할 때 사용
    #     이미 학습된 모델을 사용하여 새 데이터를 예측하는 단순한 데이터 분석에서는 사용할 필요 없음
    #     우리는 이미 학습된 KoGPT2 모델을 사용하여 추론을 수행하기 때문에 그래디언트 계산이 필요하지 않음
    #     따라서 메모리 절약을 위해 그래디언트를 비활성화
    #     """
    #     with torch.no_grad():       
    #         last_hidden_states = model(text, return_dict=True).last_hidden_state
    #         embeddings.append(last_hidden_states.mean(axis=1).flatten().numpy())

    # tfidf_vectorizer = TfidfVectorizer()
    # tfidf_matrix = tfidf_vectorizer.fit_transform(movies_df['description'])

    # # 유사도 계산
    # similarity_matrix = cosine_similarity(embeddings, tfidf_matrix)

    #    # 대상 영화들과 유사한 영화 추천
    # movie_ids = list(movies_df['id'])
    # target_movie_indices = [movie_ids.index(movie_id) for movie_id in target_movie_ids]

    # # 유사도 합산을 위한 딕셔너리 초기화
    # movie_scores = {i: 0 for i in range(len(movies_df))}

    # # 각 대상 영화에 대해 유사도 점수를 합산
    # for target_movie_index in target_movie_indices:
    #     similar_movies_indices = similarity_matrix[target_movie_index].argsort()[-2::-1]  # 자기 자신 제외하고 유사한 순서대로
    #     for index in similar_movies_indices:
    #         if index != target_movie_index:
    #             movie_scores[index] += similarity_matrix[target_movie_index][index]

    # # 유사도 점수를 기준으로 내림차순 정렬
    # sorted_movie_indices = sorted(movie_scores, key=movie_scores.get, reverse=True)

    # # 추천 결과를 영화 제목 리스트로 변환 (추천 수는 10개로 제한)
    # recommended_movies = [movies_df.iloc[index]['title'] for index in sorted_movie_indices[:10] if index not in target_movie_indices]

    # # 예시로, 추천 결과를 출력하는 템플릿에 전달
    # # return render(request, 'recommendations.html', {'recommended_movies': recommended_movies})