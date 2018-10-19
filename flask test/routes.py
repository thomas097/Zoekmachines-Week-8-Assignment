from flask import Flask, request, render_template
from simple_search import *
from advanced_search import *
from word_cloud import *
from timeline import new_timeline
import matplotlib

matplotlib.use('Agg')

app = Flask(__name__)
app.secret_key = "sdfw4h53jq"

PATH = ""
DEBUG = True
result = None


# route to homepage
@app.route('/')
def index():
    # content to display on the homepage
    home_page_content = []
    return render_template("index.html", content=home_page_content)


# enables live recommendation
@app.route('/gethint.php', methods=["GET", "POST"])
def phpexample(q="", artist="", lyrics="", songtitle=""):
    global result
    q = request.args.get("q", q)
    artist = request.args.get("artist", artist)
    songtitle = request.args.get("songtitle", songtitle)
    lyrics = request.args.get("lyrics", lyrics)

    # if user gives values to advanced search do advanced else use simple
    if artist or songtitle or lyrics:
        tempres, res = advanced_search_must(es, 'songs', lyrics, songtitle, artist, N=10, snip_size=20)
    else:
        tempres, res = simple_search(es, 'songs', q, N=10, snip_size=20)

    result = {x[0]: {"artist": x[2], "song": x[1], "genre": x[3], "year": x[4], "lyricssnip": x[5], "lyrics": x[6]} for
              x in tempres}

    resultstring = ""
    for x in tempres[:5]:
        resultstring += "<a href=\"../result/" + x[0] + "\"><li>" + x[2] + ": " + x[1] + "</li></a>"
    return resultstring


# if specific live recommendation is clicked
@app.route('/result/<q>')
def parse_results(q=""):
    if q in result:
        values = result[q]
    else:
        values, key = {}, []
    return render_template("result.html", result={q: values})


# route if answer for query is not selected from recommendations
@app.route('/search/', methods=["GET", "POST"])
def search(q="", lyrics="", artist="", songtitle=""):
    q = request.args.get("q", q)
    artist = request.args.get("artist", artist)
    song_title = request.args.get("songtitle", songtitle)
    lyrics = request.args.get("lyrics", lyrics)

    tempres, res = advanced_search_must(es, 'songs', lyrics, song_title, artist, N=10000, snip_size=20)

    # get timeline for query and query cloud for top 10
    if res['hits']['hits']:
        figure = new_timeline(res)
        wordcloud = query_cloud(es, [x[6] for x in tempres[:10]], figure)
    else:
        figure = ""
        wordcloud = ""

    # convert to usable dictionary
    tempres = {x[0]: {"artist": x[2], "song": x[1], "genre": x[3], "year": x[4], "lyricssnip": x[5],
                      "lyrics": x[6]} for x in tempres[:10]}

    return render_template("search.html", result=[tempres, figure, wordcloud])


if __name__ == "__main__":
    app.run(debug=DEBUG)
