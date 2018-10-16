from flask import Flask, request, render_template
from simple_search import *

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
def phpexample(q=""):
    global result
    q = request.args.get("q", q)

    # get 5 best matches for search query
    tempres = simple_search(es, 'songs', q, N=5, snip_size=20)
    result = {x[0]: {"artist": x[2], "song": x[1], "genre": x[3], "year": x[4], "lyrics": x[5]} for x in tempres}

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


# route if answer for query is not directly found
@app.route('/search/', methods=["GET", "POST"])
def search1(q=""):
    q = request.args.get("q", q)
    tempres = simple_search(es, 'songs', q, N=10, snip_size=20)

    # convert to usable dictionary
    tempres = {x[0]: {"artist": x[2], "song": x[1], "genre": x[3], "year": x[4], "lyrics": x[5]} for x in tempres}

    return render_template("search.html", result=tempres)


if __name__ == "__main__":
    app.run(debug=DEBUG)
