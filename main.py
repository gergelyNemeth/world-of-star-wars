from flask import Flask, render_template
import requests

app = Flask(__name__)


@app.route('/')
def root():
    response = requests.get('https://swapi.co/api/planets/').json()
    print(response)
    return render_template("star_wars.html")


if __name__ == '__main__':
    app.run(debug=True)
