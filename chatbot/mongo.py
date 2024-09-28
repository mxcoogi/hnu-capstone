from pymongo import MongoClient
import pandas as pd

# MongoDB 연결
client = MongoClient(host='localhost', port=27017)
db = client['local']
collection = db['hnu']

# 데이터 로드
df = pd.read_csv('./data/announcement_hnu2.csv', encoding='utf-8')


# 데이터 리스트 준비
ls = []
for index, row in df.iterrows():
    data = {
        'title': row['title'],
        'date': row['date'],
        'content': row['content'],
        'category': row['category'],
        'link': row['link'],
    }
    ls.append(data)

if ls:
    res = collection.insert_many(ls)
    print('complete')
else:
    print('No data')
