from elasticsearch import Elasticsearch, helpers
from wordcloud import WordCloud
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

'''
    Usage:
        1) start elastic search
        2) run function simple_search()
        3) (optional) call from demo
'''


# returns N most notable words from the docs
def word_cloud(es, index, lyrics, fname, k=4):
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
    top_terms = ' '.join([x[1] for x in top_terms])

    # create word cloud image
    wordcloud = WordCloud(background_color='white').generate(top_terms)

    # save to disk
    fig, ax = plt.subplots()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    fig.savefig(fname)


# init elastic search
es = Elasticsearch(hosts=['http://localhost:9200/'])
word_cloud(es, 'songs', 'born to be alive but this chigga isnt',
           fname='wordcloud.png')

