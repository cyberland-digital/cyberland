from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from .config import DevConfig

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.sqlite'

db = SQLAlchemy(app)


class board(db.Model):
    id = db.Column('board_id', db.Integer, primary_key=True)
    name = db.Column(db.String(1))


class posts(db.Model):
    id = db.Column('post_id', db.Integer, primary_key=True)
    content = db.Column('post_content', db.String(10000))
    reply_to = db.Column('reply_to', db.ForeignKey(), nullable=True)


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
