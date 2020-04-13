from flask import Blueprint, flash, g, render_template, request, make_response, jsonify

from flaskr.db import get_db

# Helper functions


def serve_text(file):
    response = make_response(render_template(file))
    response.mimetype = "text/plain"
    return response, 200


def process_request(board, req):
    if request.method == 'POST':
        content = req.form.get('content')
        replyto = req.form.get('replyTo')

        db = get_db()
        # validate the request and determine weather is reply or op
        if replyto:
            # check that post with that id exists for that board
            pass
        else:
            post = db.execute('insert into post (board, content) values (?, ?)', (board, content))
            db.commit()
            return jsonify(post), 201


def create_post(board, content):
    pass


def get_posts(board, num, thread):
    pass

# Controllers


bp = Blueprint('post', __name__, url_prefix='/')


@bp.route('/')
def index():
    return serve_text("index.txt")


@bp.route("/tut.txt")
def tut():
    return serve_text("tut.txt")

# board routes


@bp.route("/n/", methods=['GET', 'POST'])
@bp.route("/n", methods=['GET', 'POST'])
def board_n():
    if request.method == 'POST':
        board = 'n'
        content = request
        process_request(board,request)


@bp.route('/o/', methods=['GET', 'POST'])
@bp.route('/o', methods=['GET', 'POST'])
def board_o():
    return '''\nWelcome to board /o/. \n
Please use Get and Post requests directly to interact with this board.\n\n''', 200


@bp.route('/t/', methods=['GET', 'POST'])
@bp.route('/t', methods=['GET', 'POST'])
def board_t():
    return 'placeholder text'
