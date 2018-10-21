from elasticsearch import Elasticsearch, helpers
from collections import Counter
from pprint import pprint
import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import string
from random import *
import os

'''
    Usage:
        1) start elastic search
        2) run function timeline()
        3) (optional) call from demo
'''

# removes all images in images to prevent overdosis of images
def clear_images():
    folder = './static/images/'
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)

def new_timeline(res):
    clear_images()
    # determine number of documents (that match the query) with a particular year
    counts = Counter([int(x['_source']['year']) for x in res['hits']['hits']])
    years, counts = zip(*sorted(counts.items()))

    # create figure and save to path
    fig, ax = plt.subplots(figsize=(10, 2))
    # ax.set_yticklabels([])
    # plt.plot(years, counts, 'b-')
    ax.bar(years, counts, .5, color='#a80000')

    # prevent using cached images over and over again
    random_string = "".join(choice(string.ascii_letters) for x in range(5))

    fig.savefig('./static/images/timeline' + str(random_string) + '.png')
    return str(random_string)



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
#es = Elasticsearch(hosts=['http://localhost:9200/'])
#timeline(es, 'songs', '', '', 'james bay', 'timeline.png')

