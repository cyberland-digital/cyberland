from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os


# App config
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

# Controllers


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/tut.txt")
def tut():
    return render_template("tut.html")


@app.route("/o", methods=["GET", "POST"])
def board_o():
    # hn
    return ('<b>Welcome to board /t', 200)


@app.route('/t')
def board_t():
    return ('<b>Welcome to board /t', 200)

# Error handlers


@app.errorhandler(404)
def not_found_error(error):
    return ('<b>Page not found</b>', 404)


if __name__ == '__main__':
    app.run()
