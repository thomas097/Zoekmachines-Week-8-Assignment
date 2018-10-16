from elasticsearch import Elasticsearch, helpers
from pprint import pprint
import re

'''
    Usage:
        1) start elastic search
        2) run function simple_search()
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
# returns N tuples of (docID, title, artist, genre, year, lyrics snippet)
def simple_search(es, index, query, N=10, snip_size=20):
    # define query with conjunctive semantics (as opposed to disjunctive)
    dict_query = {"query":{
                       "match":{
                            "lyrics":{
                                "query":query,
                                "operator":"and"
                                }
                           }
                       },
                  "size":N}
    # pose query to system
    res = es.search(index=index, body=dict_query)
    # format results
    results_list = []
    for hit in res['hits']['hits']:
        song = hit['_source']
        hit = (hit['_id'], song['song_title'], song['artist'], song['genre'],
               song['year'], create_snippet(song['lyrics'], query, snip_size))
        results_list.append(hit)
    return results_list


# init elastic search
es = Elasticsearch(hosts=['http://localhost:9200/'])
res = simple_search(es, 'songs', 'all the single ladies', N=10, snip_size=20)
pprint(res)

