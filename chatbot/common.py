import config
from openai import OpenAI
from dataclasses import dataclass
import pytz
from datetime import datetime
import config, json, faiss
import numpy as np



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

with open('./data/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

index = faiss.read_index('./data/faiss_index.index')

def vectorize(text):
    response = client.embeddings.create(input=text, model='text-embedding-ada-002')
    return np.array(response.data[0].embedding).astype('float32')