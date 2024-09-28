from sentence_transformers import SentenceTransformer

# 모델 로드
model = SentenceTransformer('snunlp/KR-SBERT-V40K-klueNLI-augSTS')

def to_vector(data):
    combined_text = f"title: {data['title']} | date: {data['date']} | content: {data['content']} | category: {data['category']} | link: {data['link']}"
    res = model.encode(combined_text)
    return res
        