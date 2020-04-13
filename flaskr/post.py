from flask import Blueprint, render_template, request, make_response
from flask_limiter import Limiter
from json import dumps

from flaskr.db import get_db


# Helper functions


def prepare_json(data):
    if type(data) == list:
        json_string = dumps([dict(row) for row in data], default=str)
    else:
        json_string = dumps(dict(data), default=str)
    json_string = make_response(json_string)
    json_string.mimetype = "application/json"
    return json_string, 200


def serve_text(file):
    response = make_response(render_template(file))
    response.mimetype = "text/plain"
    return response, 200


def process_request(board, req):
    db = get_db()
    if request.method == 'POST':
        content = req.form.get('content')
        reply = req.form.get('replyTo')

        db.execute('insert into {} (content, replyTo) values (?, ?)'.format(board), (content, reply))
        db.commit()

        # If it is replying to a post (not an OP) then it must bump it
        if reply:
            reply = int(reply)
            db.execute('update {} set bumpCount = bumpCount + 1 where id = ?'.format(board), (reply,))
            db.commit()

        data = db.execute('select * from {} order by time desc limit ?'.format(board), (50,)).fetchall()
        return prepare_json(data)

    elif request.method == 'GET':
        sort = req.args.get('sort')
        num = req.args.get('num')
        thread = req.args.get('thread')
        if not sort:
            sort = "time"
        if not num:
            num = 50
        if thread:
            data = db.execute('select * from {} where replyTo=? or id=? order by ? desc limit ?'.format(board),
                                (thread, thread, sort, num)).fetchall()

        else:
            data = db.execute('select * from {} order by ? desc limit ?'.format(board), (sort, num)).fetchall()

        return prepare_json(data)


bp = Blueprint('post', __name__)

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
