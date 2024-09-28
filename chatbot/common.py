import config
from openai import OpenAI
from dataclasses import dataclass
import pytz
from datetime import datetime
import pickle
import faiss
from langchain_openai import OpenAIEmbeddings
import config

# FAISS 인덱스 로드
index = faiss.read_index('faiss_index.index')

# 원본 데이터 로드
with open('notices.pkl', 'rb') as f:
    id_text_pairs = pickle.load(f)

embeddings_function = OpenAIEmbeddings(
    model='text-embedding-3-large', 
    openai_api_key=config.api_key
)
ids, texts = zip(*id_text_pairs)

def today():
    korea = pytz.timezone('Asia/Seoul')
    now = datetime.now(korea)
    return (now.strftime("%Y%m%d"))

def current():
    korea = pytz.timezone('Asia/Seoul')
    now = datetime.now(korea)
    formatted_now = now.strftime("%Y.%m.%d %H:%M:%S")
    return formatted_now
    
def makeup_response(message, finish_reason="ERROR"):
    return {
                "choices": [
                    {
                        "finish_reason": finish_reason,
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": message
                        }
                    }
                ],
                "usage": {"total_tokens": 0},
            }

@dataclass(frozen= True)
class Model:
    basic : str = "gpt-3.5-turbo-1106"
    advanced : str = "gpt-4-1106-preview"

model = Model();  
client = OpenAI(api_key=config.api_key, timeout=30, max_retries=1)
