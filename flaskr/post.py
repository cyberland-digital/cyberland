from flask import Blueprint, render_template, request, make_response, jsonify
import json
import sqlite3

from flaskr.db import get_db


# Helper functions


def serve_text(file):
    response = make_response(render_template(file))
    response.mimetype = "text/plain"
    return response, 200


def process_request(board, req):
    if request.method == 'POST':
        content = req.args.get('content')
        reply = int(req.args.get('replyTo'))

        cur = get_db().execute('insert into ? (content, replyTo) values (?, ?)', (content, reply))
        # If it is replying to a post (not an OP) then it must bump it
        if reply:
            cur = get_db().execute('update ? set bumpCount = bumpCount + 1 where id = ?', (reply))
        get_db().commit()

        return 'hi'

    elif request.method == 'GET':
        db = get_db()
        db.row_factory = sqlite3.Row

        cur = db.cursor()

        num = req.args.get('num')
        thread = req.args.get('thread')
        if not num:
            num = 50
        if thread:

            data = cur.execute('select * from {} where replyTo=? or id=? order by bumpCount desc limit ?'.format(board),
                               (thread, thread, num)).fetchall()

        else:
            data = cur.execute('select * from {} order by bumpCount desc limit ?'.format(board), (num,)).fetchall()
            cur.close()
        cur.close()
        return jsonify([dict(row) for row in data])


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
