from flask import Blueprint, render_template, request, make_response, jsonify
from flask_limiter import Limiter

from flaskr.db import get_db


# Helper functions


def prepare_json(data):
    if type(data) == list:
        json_string = jsonify([dict(row) for row in data])
    else:
        json_string = jsonify(dict(data))
    return json_string


def serve_text(file):
    response = make_response(render_template(file))
    response.mimetype = "text/plain"
    return response, 200


def process_request(board, req):
    db = get_db()
    if request.method == 'POST':

        content = req.form.get('content')
        print(content)
        reply = req.form.get('replyTo')

        db.execute('insert into {} (content, replyTo) values (?, ?)'.format(board), (content, reply))
        db.commit()

        # If it is replying to a post (not an OP) then it must bump it
        if reply:
            reply = int(reply)
            db.execute('update {} set bumpCount = bumpCount + 1 where id = ?'.format(board), (reply,))
            db.commit()

        data = db.execute('select * from {} order by created desc limit ?'.format(board), (50,)).fetchall()
        return prepare_json(data)

    elif request.method == 'GET':

        num = req.args.get('num')
        thread = req.args.get('thread')

        if not num:
            num = 50
        if thread:
            data = db.execute('select * from {} where replyTo=? or id=? order by created desc limit ?'.format(board),
                              (thread, thread, num)).fetchall()

        else:
            data = db.execute('select * from {} order by created desc limit ?'.format(board), (num,)).fetchall()

        return prepare_json(data)


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
    return process_request('news', request)


@bp.route('/o/', methods=['GET', 'POST'])
@bp.route('/o', methods=['GET', 'POST'])
def board_o():
    return process_request('offtopic', request)


@bp.route('/t/', methods=['GET', 'POST'])
@bp.route('/t', methods=['GET', 'POST'])
def board_t():
    return process_request('tech', request)


@bp.route('/i/', methods=['GET', 'POST'])
@bp.route('/i', methods=['GET', 'POST'])
def board_i():
    return process_request('images', request)
