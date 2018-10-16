from elasticsearch import Elasticsearch, helpers
from pprint import pprint
import re
import numpy as np

'''
    Usage:
        1) start elastic search
        2) run function simple_search()
        3) (optional) call from demo
'''


# returns N most notable words from the docs
def word_cloud(es, index, lyrics, k=3):
    # determine size of index (document count)
    N = es.count(index=index)['count']
    # return k most
    scores = []
    for t in set(lyrics.split(' ')):
        res = es.count(index=index, body={"query":{"term":{"lyrics":t}}})
        idf = np.log(N/res['count'])
        scores.append((idf, t))
    # grab top words according to idf
    top_terms = sorted(scores, key=lambda x: -x[0])[:k]
    return top_terms


# init elastic search
es = Elasticsearch(hosts=['http://localhost:9200/'])
res = word_cloud(es, 'songs', 'born to be alive')
print(res)
