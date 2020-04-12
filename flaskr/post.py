from flask import Blueprint, flash, g, render_template, request, make_response, jsonify

from flaskr.db import get_db

# Helper functions


def serve_text(file):
    response = make_response(render_template(file))
    response.mimetype = "text/plain"
    return response, 200

# Controllers


bp = Blueprint('post', __name__, url_prefix='/')


@bp.route('/')
def index():
    return serve_text("index.txt")


@bp.route("/tut.txt")
def tut():
    return serve_text("tut.txt")


@bp.route("/n/")
@bp.route("/n")
def board_n():
    return '''\nWelcome to board /n/. \n
Please use Get and Post requests directly to interact with this board.\n\n''', 200


@bp.route('/o/')
@bp.route('/o')
def board_o():
    return '''\nWelcome to board /o/. \n
Please use Get and Post requests directly to interact with this board.\n\n''', 200


@bp.route('/t', methods=['GET'])
def board_t():
    return 'placeholder text'


# Error handlers



