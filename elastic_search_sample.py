from elasticsearch import Elasticsearch, helpers

index = 'test-index'
_type = 'song'

doc1 = {
    '_index' : index,
    '_type' : _type,
    '_source' : {
        'artist' : 'mgk',
        'lyrics' : 'lolololol.',
        'diss' : 'yes',
        'year' : 2018
    }
}

doc2 = {
    '_index' : index,
    '_type' : _type,
    '_source' : {
        'artist' : 'hello',
        'lyrics' : 'yas... words things',
        'diss' : 'yes',
        'year' : 2018
    }
}

doc3 = {
    '_index' : index,
    '_type' : _type,
    '_source' : {
        'artist' : 'hi',
        'lyrics' : 'more words',
        'diss' : 'yes',
        'year' : 2018
    }
}

docs = [doc1, doc2, doc3]




# init elastic search
es = Elasticsearch(hosts=['http://localhost:9200/'])

# clear index if it exists
es.indices.delete(index=index, ignore=[400, 404])

# index file
helpers.bulk(es, docs)

# refresh to have the index take effect
es.indices.refresh(index=index)

# try search
res = es.search(index=index, body={"query": {"match": {'lyrics':'more words'}}})

# print hits
print("Got %d Hits:" % res['hits']['total'])
for i, hit in enumerate(res['hits']['hits']):
    print(i, "   %(year)s %(artist)s: %(lyrics)s" % hit["_source"])
