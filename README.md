# Zoekmachines-Week-8-Assignment
This repository contains the Elastic Search asignment for Zoekmachines 2018. The project is described in-depth on the following wiki page:


https://github.com/thomas097/Zoekmachines-Week-8-Assignment/wiki/Zoekmachines-Elastic-Search-Assignment

``` Progress:
Index: dun (alleen nog evereenstemmen met welke data we precies willen / hoe we pre-processen en of we expanden (kan later))
Q1: dun (behalve dat het nog niet in een demo zit / afhankelijk van verdere implementaties voor de rest van de vragen)
Q2: ?
Q3: ?
Q4: ?
Q5: ?
Q6: ?
Demo: Sampletje met Flask
```



{"query": 
    {"bool":
        { "must":
            {"query_string":
                {"fields":["song_title", "artist^5"], "query": query}
            }, 
            {"filter":
                {"range":{"year":{"gte":2017}}}
            }
        }
    }, "size":N
})

{"query": {"bool":{ "must":{"query_string":{"fields":["song_title", "artist^5"], "query": query}}, {"filter":{"range":{"year":{"gte":2017}}}}}}, "size":N})