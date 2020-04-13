from flask import Blueprint, render_template, request, make_response, jsonify

from flaskr.db import get_db


# Helper functions


def serve_text(file):
    response = make_response(render_template(file))
    response.mimetype = "text/plain"
    return response, 200


def process_request(board, req):
    db = get_db()
    if request.method == 'POST':
        content = req.args.get('content')
        reply = req.args.get('replyTo')

        db.execute('insert into ? (content, replyTo) values (?, ?)', (board, content, reply))
        # If it is replying to a post (not an OP) then it must bump it
        if reply:
            db.execute('update ? set bumpCount = bumpCount + 1 where id = ?', (board, reply))
        db.commit()

        return 'object created', 201

    elif request.method == 'GET':
        num = int(req.args.get('content'))
        thread = str(req.args.get('thread'))

        if thread:
            posts = db.execute('select * from ? where replyTo=? or id=? order by bumpCount desc limit ?',
                               (board, thread, thread, num)).fetchall()
        else:
            posts = db.execute('select * from ? where replyTo')
        return jsonify(posts)


bp = Blueprint('post', __name__, url_prefix='/')


# help files


@bp.route('/')
def index():
    return serve_text("index.txt")


@bp.route("/tut.txt")
def tut():
    return serve_text("tut.txt")


# boards


@bp.route("/n/", methods=['GET', 'POST'])
@bp.route("/n", methods=['GET', 'POST'])
def board_n():
    board = 'news'
    process_request(board)


@bp.route('/o/', methods=['GET', 'POST'])
@bp.route('/o', methods=['GET', 'POST'])
def board_o():
    board = 'offtopic'


@bp.route('/t/', methods=['GET', 'POST'])
@bp.route('/t', methods=['GET', 'POST'])
def board_t():
    board = 'tech'
