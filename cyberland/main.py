from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/tut.txt")
def tut():
    return render_template("tut.html")

@app.route("/t", methods=["GET", "POST"])
@app.route("/o", methods=["GET", "POST"])
def board():
    # 

if __name__ == '__main__':
    app.run()
