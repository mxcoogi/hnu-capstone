import numpy as np
import faiss
from pymongo import MongoClient
from langchain_openai import OpenAIEmbeddings
import config
import pickle

embeddings_function = OpenAIEmbeddings(model = 'text-embedding-3-large', openai_api_key=config.api_key)

# MongoDB 클라이언트 생성
mongo_client = MongoClient(host='localhost', port=27017)
db = mongo_client['local']
collection = db['hnu']

# 데이터 가져오기 및 벡터화
documents = collection.find()
texts = []
ids = []  # 원문 ID 저장
for document in documents:
    title = document.get('title', '')
    date = document.get('date', '')
    content = document.get('content', '') if document.get('content') is not None else ''
    category = document.get('category', '')
    link = document.get('link', '')
    
    full_text = f"Title: {title} | Date: {date} | Category: {category} | Content: {content} | Link: {link}".strip()
    
    if full_text:
        texts.append(full_text)
        ids.append(str(document['_id']))  # ID 추가 (문자열로 변환)

vectors = np.array([embeddings_function.embed_query(text) for text in texts]).astype('float32')

dimension = vectors.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(vectors)

# FAISS 인덱스를 디스크에 저장
faiss.write_index(index, 'faiss_index.index')

with open('notices.pkl', 'wb') as f:
    pickle.dump(list(zip(ids, texts)), f)