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

# Parses the searech query in a query suitable for the elastic search.
# def create_search(song, artist):
#     for word in query.split():
#         if word == 'or':

#         if word == 'and':


# implements simple keyword search in the indexed lyrics
# returns N tuples of (title, artist, genre, year, lyrics snippet)
def harder_simple_search(es, index, lyrics, artist, N=10, snip_size=20):
    query = lyrics + " and " + artist
    res = es.search(index=index, body={"query": {"query_string": {"fields": ["song_title", "artist"], "query": query}}, "size":N})
    results_list = []
    for hit in res['hits']['hits']:
        song = hit['_source']
        hit = (song['song_title'], song['artist'], song['genre'], song['year'],
               create_snippet(song['lyrics'], query, snip_size))
        results_list.append(hit)
    return results_list


# init elastic search
es = Elasticsearch(hosts=['http://localhost:9200/'])
res1 = simple_search(es, 'songs', 'ik wil graag een nummer met single-ladies AND beyonce', N=10, snip_size=20)
res2 = harder_simple_search(es, 'songs', 'zij gelooft in mij', 'Andre Hazes', N=10, snip_size=20)
pprint(res2)
