from elasticsearch import Elasticsearch, helpers
from pprint import pprint
import re

'''
    Usage:
        1) start elastic search
        2) run function advanced_search()
        3) (optional) call from demo
'''


# creates a snippet containing the most amount of words from the query
def create_snippet(lyrics, query, length):
    query_terms = set(query.split(' '))
    lyrics_terms = lyrics.replace('\n', ' ').split(' ')
    
    # loop over ngrams and return the one with the most query terms
    snippet, score = '', -1
    for i in range(len(lyrics_terms)-length+1):
        new_snippet = lyrics_terms[i:i+length]
        new_score = len(set(new_snippet).intersection(query_terms))
        if new_score >= score:
            snippet = ' '.join(new_snippet)
            score = new_score
    return snippet


# implements simple keyword search in the indexed lyrics
def advanced_search(es, index, lyrics, artist, N=10, snip_size=20):
    query =  '({}) and ({})'.format(' or '.join(lyrics), ' or '.join(artist))
    print(query)
    res = es.search(index=index, body={
        "query": {
            "bool":{
                "must":{
                    "query_string":{
                        "fields":["song_title", "artist"],
                        "query": query
                    }
                }
            }
        },
        "size":N
    })
    results_list = []
    for hit in res['hits']['hits']:
        song = hit['_source']
        hit = (hit['_id'], song['song_title'], song['artist'], song['genre'], song['year'],
               create_snippet(song['lyrics'], query, snip_size))
        results_list.append(hit)
    return results_list


# init elastic search
es = Elasticsearch(hosts=['http://localhost:9200/'])
res = advanced_search(es, 'songs', ['single ladies', 'halo'], ['Beyonce', 'Andre'], N=10, snip_size=20)
pprint(res)
