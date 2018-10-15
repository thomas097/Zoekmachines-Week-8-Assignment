from elasticsearch import Elasticsearch, helpers
from tqdm import tqdm
import pandas as pd

'''
    USAGE:
    1) download metrolyrics data set
    2) extract file in same folder where this file is located
    3) start elastic search from Downloads/elasticsearch-.6.4.2
       with ./bin/elasticsearch (may take a minute to boot up)
    3) run this script
'''

# define index name and document type
index = 'songs'
_type = 'song'

# load metrolyrics dataset into pandas DataFrame
df_cols = ['title', 'year', 'artist', 'genre', 'lyrics']
df = pd.read_csv('380000-lyrics-from-metrolyrics/lyrics.csv', dtype=str,
                 sep=',', usecols=[1, 2, 3, 4, 5], names=df_cols)
df = df.dropna()
print(df.shape)

# TODO: pre-processing

# convert each song into elastic search format and append to list of docs
docs = []
for i, row in tqdm(df.iterrows()):
    doc = {
        '_index' : index,
        '_type' : _type,
        '_source' : {
            'song_title' : row['title'],
            'year' : row['year'],
            'artist' : row['artist'],
            'genre' : row['genre'],
            'lyrics' : row['lyrics'],
        }
    }
    docs.append(doc)

# init elastic search API
es = Elasticsearch(hosts=['http://localhost:9200/'])

# clear index if it exists
if es.indices.exists(index=index):
    es.indices.delete(index=index)#, ignore=[400, 404])
    print('Previous version of index removed!\nReplacing with new!')

# index file
helpers.bulk(es, docs)

# refresh to have the index take effect
es.indices.refresh(index=index)

# DONE!

