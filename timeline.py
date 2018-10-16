from elasticsearch import Elasticsearch, helpers
from collections import Counter
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np

'''
    Usage:
        1) start elastic search
        2) run function timeline()
        3) (optional) call from demo
'''


# implements simple keyword search in the indexed lyrics
# returns N tuples of (docID, title, artist, genre, year, lyrics snippet)
def timeline(es, index, query, fname):
    # define query to obtain the release dates of 10000 songs
    dict_query = {"_source": ["year"],
                  "query":{
                      "match":{
                          "lyrics":{
                              "query":query,
                              "operator":"and"
                              }
                          }
                      },
                  "stored_fields":['year'],
                  "size":10000}
    
    # pose query to system to obtain at most 10000 years (of docs) 
    res = es.search(index=index, body=dict_query)
    
    # determine number of documents (that match the query) with a particular year
    counts = Counter([int(x['_source']['year']) for x in res['hits']['hits']])
    years, counts = zip(*sorted(counts.items()))

    # normalize counts
    total = sum(counts)
    counts = [c/total for c in counts]

    # create figure and save to disk as fname
    fig, ax = plt.subplots()
    ax.set_yticklabels([])
    plt.plot(years, counts, 'b-')
    ax.fill_between(years, 0, counts, color='b') 
    fig.savefig(fname)


# init elastic search
es = Elasticsearch(hosts=['http://localhost:9200/'])
timeline(es, 'songs', 'swag', 'timeline.png')

