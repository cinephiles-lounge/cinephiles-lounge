from transformers import BertModel, BertTokenizer
import torch

# KoBERT 모델과 토크나이저 로드
tokenizer = BertTokenizer.from_pretrained('monologg/kobert')
model = BertModel.from_pretrained('monologg/kobert')

def get_embedding(text):
    inputs = tokenizer(text, return_tensors='pt')
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()

korean_texts = ["안녕하세요", "반갑습니다", "오늘 날씨가 좋네요"]
embeddings = [get_embedding(text) for text in korean_texts]


import faiss
import numpy as np

# 임베딩 배열을 FAISS 인덱스에 추가
d = embeddings[0].shape[1]
index = faiss.IndexFlatL2(d)
index.add(np.vstack(embeddings))

# 검색할 한국어 문장을 벡터화
query = "안녕"
query_embedding = get_embedding(query)

# 유사도 검색
k = 2  # 상위 2개의 유사한 결과를 찾습니다.
D, I = index.search(query_embedding, k)
print(I)  # 유사한 문장의 인덱스 출력