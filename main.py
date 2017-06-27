from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def planets(url="https://swapi.co/api/planets/"):
    if request.method == "POST":
        if request.form['url'] != "None":
            url = request.form['url']
    response = requests.get(url).json()
    planets = response["results"]
    prev_page = response["previous"]
    next_page = response["next"]

    return render_template("star_wars.html", planets=planets, len=len, int=int, format=format,
                           prev_page=prev_page, next_page=next_page)

if __name__ == '__main__':
    app.run(debug=True)
