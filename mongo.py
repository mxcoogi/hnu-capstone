from pymongo import MongoClient
import pandas as pd
from to_vector import to_vector
client = MongoClient(host = 'localhost', port = 27017)
#print(client.list_database_names())
db = client['local']
collection = db['hnu']

data = {
	'title' : 'value',
	'date': 'YYYY-MM-DD hh:mm',
	'content' : 'value',
	'category' : 'value',
    'link' : 'link'    
}
df = pd.read_csv('./data/announcement_hnu2.csv', encoding='utf-8').head()
ls = []
for index, row in df.iterrows():
    data = {
	'title' : row['title'],
	'date': row['date'],
	'content' : row['content'],
	'category' : row['category'],
    'link' : row['link']    
    }
    res = to_vector(data)
    ls.append(res)
