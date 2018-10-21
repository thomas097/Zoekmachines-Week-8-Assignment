from elasticsearch import Elasticsearch, helpers
from wordcloud import WordCloud
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

'''
    Usage:
        1) start elastic search
        2) run function word_cloud()
        3) (optional) call from demo
'''


# returns N most notable words from the docs
def word_cloud(es, index, lyrics, path, k=4):
    # determine the total number of indexed documents
    N = es.count(index=index)['count']
    
    # determine for each term occurring in the returned songs and 
    # IDF value (indicating its relevance to the word cloud)
    scores = []
    for t in set(lyrics.split(' ')):
        res = es.count(index=index, body={"query":{"term":{"lyrics":t}}})
        idf = np.log(N/res['count'])
        scores.append((idf, t))
        
    # grab top k terms w.r.t. to their IDF value
    top_terms = sorted(scores, key=lambda x: -x[0])[:k]
    top_terms = ' '.join([x[1] for x in top_terms])

    # create word cloud image using WordCliud library
    wordcloud = WordCloud(background_color='white').generate(top_terms)

    # store image in path
    fig, ax = plt.subplots()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    fig.savefig(path)


# init elastic search
es = Elasticsearch(hosts=['http://localhost:9200/'])
word_cloud(es, 'songs', 'lose yourself in the music the moment you own it',
           path='wordcloud.png')

