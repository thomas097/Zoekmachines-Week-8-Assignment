from elasticsearch import Elasticsearch, helpers
from collections import Counter
from pprint import pprint
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import string
from random import *

'''
    Usage:
        1) start elastic search
        2) run function timeline()
        3) (optional) call from demo
'''


def new_timeline(res):
    # determine number of documents (that match the query) with a particular year
    counts = Counter([int(x['_source']['year']) for x in res['hits']['hits']])
    years, counts = zip(*sorted(counts.items()))

    # create figure and save to path
    fig, ax = plt.subplots(figsize=(10,2))
    ax.set_yticklabels([])
    plt.plot(years, counts, 'b-')
    ax.fill_between(years, 0, counts, color='b')

    # prevent using cached images over and over again
    random_string = "".join(choice(string.ascii_letters) for x in range(5))

    fig.savefig('./static/images/timeline'+str(random_string)+'.png')
    return str(random_string)


# implements simple keyword search in the indexed lyrics
# returns N tuples of (docID, title, artist, genre, year, lyrics snippet)
def timeline(es, index, query, path):
    # define query to obtain the release dates of 10000 songs
    dict_query = {"_source": ["year"],
                  "query": {
                      "match": {
                          "lyrics": {
                              "query": query,
                              "operator": "and"
                          }
                      }
                  },
                  "stored_fields": ['year'],
                  "size": 10000}

    # pose query to system to obtain at most 10000 years (of docs) 
    res = es.search(index=index, body=dict_query)

    # determine number of documents (that match the query) with a particular year
    counts = Counter([int(x['_source']['year']) for x in res['hits']['hits']])
    years, counts = zip(*sorted(counts.items()))

    # create figure and save to path
    fig, ax = plt.subplots()
    ax.set_yticklabels([])
    plt.plot(years, counts, 'b-')
    ax.fill_between(years, 0, counts, color='b')
    fig.savefig(path)


# init elastic search
es = Elasticsearch(hosts=['http://localhost:9200/'])
# timeline(es, 'songs', 'swag', './flask test/static/timeline.png')
