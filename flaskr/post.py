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
        reply = int(req.args.get('replyTo'))

        post = db.execute('insert into ? (content, replyTo) values (?, ?)', (content, reply))
        # If it is replying to a post (not an OP) then it must bump it
        if reply:
            db.execute('update ? set bumpCount = bumpCount + 1 where id = ?', (reply))
        db.commit()

        return jsonify(post.fetchone()), 201

    elif request.method == 'GET':
        print('running this 1')
        num = req.args.get('num')
        thread = req.args.get('thread')
        if not num:
            num = 50
        if thread:
            posts = db.execute('select * from {} where replyTo=? or id=? order by bumpCount desc limit ?'.format(board),
                               (thread, thread, num)).fetchall()
        content = req.form.get('content')
        replyto = req.form.get('replyTo')

        db = get_db()
        # validate the request and determine weather is reply or op
        if replyto:
            # check that post with that id exists for that board
            pass
        else:
            posts = db.execute('select * from {} order by bumpCount desc limit ?'.format(board), (num,)).fetchall()
        print(posts)
        return jsonify(json_list=posts)


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
    return process_request(board, request)


@bp.route('/o/', methods=['GET', 'POST'])
@bp.route('/o', methods=['GET', 'POST'])
def board_o():
    board = 'offtopic'


@bp.route('/t/', methods=['GET', 'POST'])
@bp.route('/t', methods=['GET', 'POST'])
def board_t():
    board = 'tech'
