from elasticsearch import Elasticsearch, helpers
from pprint import pprint
import re

def faceted_search(es, index, facet_values):
    dict_query = {"query": {
                        "bool": {
                            "must": []
                        }
                    },
                  "aggs": {
                        "genre": {
                            "terms": {
                                "field": "genre.keyword"
                                }
                            },
                         "year": {
                            "terms": {
                                "field": "year.keyword"
                                }
                            },
                         "artist": {
                            "terms": {
                                "field": "artist.keyword"
                                }
                            },
                    },
                  "size":0
                }

    # augment query with additional facet values (if selected)
    for facet, value in facet_values:
        dict_query["query"]["bool"]["must"].append({"match":{facet:value}})
    
    res = es.search(index=index, body=dict_query)
    pprint(res)


# init elastic search
es = Elasticsearch(hosts=['http://localhost:9200/'])
faceted_search(es, 'songs', facet_values=[("lyrics", 'halo'), ('year', '2008')])

