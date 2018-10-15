from elasticsearch import Elasticsearch, helpers
from pprint import pprint

'''
    Usage:
        1) start elastic search
        2) run function simple_search()
'''


# implements simple keyword search in the indexed lyrics
# returns N tuples of (title, artist, genre, year, lyrics snippet)
def simple_search(es, index, _type, query, N=10):
    res = es.search(index=index, body={"query": {"match": {'lyrics': query}}})
    
    for hit in res['hits']['hits']:
        print(hit['_source']['artist'])
    return res

# init elastic search
es = Elasticsearch(hosts=['http://localhost:9200/'])
simple_search(es, 'songs', 'song', 'rejoice everytime you hear the sound of my voice')
