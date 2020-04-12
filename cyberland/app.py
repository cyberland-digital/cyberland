from flask import Flask, render_template, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from cyberland.models import *

# App config
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


# Controllers

def serve_text(file):
    response = make_response(render_template(file))
    response.mimetype = "text/plain"
    return response, 200


@app.route('/')
def index():
    return serve_text("index.txt")


@app.route("/tut.txt")
def tut():
    return serve_text("tut.txt")


@app.route("/n/")
@app.route("/n")
def board_n():
    return '''\nWelcome to board /n/. \n
Please use Get and Post requests directly to interact with this board.\n\n''', 200


@app.route('/o/')
@app.route('/o')
def board_o():
    return '''\nWelcome to board /o/. \n
Please use Get and Post requests directly to interact with this board.\n\n''', 200


@app.route('/t/', methods=['GET'])
@app.route('/t', methods=['GET'])
def board_t():
    results = Post.query.filter_by(board='t')
    return jsonify(results)


# Error handlers


@app.errorhandler(404)
def not_found_error(error):
    return 'Page not found\n', 404


if __name__ == '__main__':
    app.run()
