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


# implements the timeline feature by resubmitting a query, with
# a larger number of documents and only release dates.
def timeline(es, index, lyrics, song_title, artist, path):
    # define query to obtain the release dates songs
    dict_query = {"_source": ["year"],
                  "query":{
                      "bool": {
                        "should": [
                            {"match": {"lyrics": lyrics}},
                            {"match": {"song_title": song_title}},
                            {"match": {"artist": artist}}
                          ]
                      }
                  },
                  "stored_fields":['year'],
                  "size":10000}
    
    # pose query to system to obtain at most 10000 years (of docs) 
    res = es.search(index=index, body=dict_query)
    
    if len(res['hits']['hits']):
        # determine number of documents (that match the query) with a particular year
        counts = Counter([int(x['_source']['year']) for x in res['hits']['hits']])
        years, counts = zip(*sorted(counts.items()))

        # create figure and save to path
        fig, ax = plt.subplots()
        ax.set_yticklabels([])
        plt.plot(years, counts, 'b-')
        ax.fill_between(years, 0, counts, color='b') 
        fig.savefig(path)
    else:
        # signal no result
        print('No results')


# init elastic search
es = Elasticsearch(hosts=['http://localhost:9200/'])
timeline(es, 'songs', '', '', 'james bay', 'timeline.png')

