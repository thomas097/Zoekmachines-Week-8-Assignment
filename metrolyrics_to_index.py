from elasticsearch import Elasticsearch, helpers
from tqdm import tqdm
import pandas as pd

'''
    USAGE:
    1) start elastic search from Downloads/elasticsearch-.6.4.2
       with ./bin/elasticsearch (may take a minute to boot up)
    2) run this script
'''

# cleans the terrible data set format
def camelcase(string):
    return ' '.join([w[0].upper()+w[1:] for w in string.split('-')])

# define index name and document type
index = 'songs'
_type = 'song'

# load metrolyrics dataset into pandas DataFrame
df_cols = ['title', 'year', 'artist', 'genre', 'lyrics']
df = pd.read_csv('lyrics.csv', dtype=str, header=0,
                 sep=',', usecols=[1, 2, 3, 4, 5], names=df_cols)
df = df.dropna()
print(df.head(6))
print('Shape of data set;', df.shape)

# convert each song into elastic search format and append to list of docs
docs = []
for i, row in tqdm(df.iterrows()):

    # pre-process
    row['title'] = camelcase(row['title'])
    row['artist'] = camelcase(row['artist'])
    row['genre'] = camelcase(row['genre'])
    
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
    es.indices.delete(index=index)
    print('Previous version of index removed!\nReplacing with new!')
print('This may take a few minutes...')

# index file
helpers.bulk(es, docs)

# refresh to have the index take effect
es.indices.refresh(index=index)

# DONE!
print('done!')
