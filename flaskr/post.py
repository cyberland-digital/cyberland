from flask import Blueprint, render_template, request, make_response
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


def reject_request(msg):
    return msg, 400


def post_exists(db, board, id):
    data = db.execute('select distinct id from {} where id = ?'.format(board), (id,)).fetchone()
    if data:
        return True
    return False


def process_request(board, req):
    db = get_db()
    if request.method == 'POST':

        BOARD_LIMITS = {
            'tech': 10000,
            'offtopic': 10000,
            'news': 1000,
            'images': 100000
        }

        content = req.form.get('content')
        reply = req.form.get('replyTo')

        if reply == 'null':
            reply = None

        if not content:
            reject_request("Post must have content")

        if len(content) > BOARD_LIMITS[board]:
            reject_request(f"The character limit for this board is {BOARD_LIMITS[board]}")

        db.execute('insert into {} (content, replyTo) values (?, ?)'.format(board), (content, reply))
        db.commit()

        if not post_exists(db, board, reply):
            reject_request('The post you are replying to does not exist')

        # If it is replying to a post (not an OP) then bump
        if reply:
            db.execute('update {} set bumpCount = bumpCount + 1 where id = ?'.format(board), (reply,))
            db.commit()

        data = db.execute('select * from {} order by id desc limit ?'.format(board), (50,)).fetchall()
        return prepare_json(data)

    elif request.method == 'GET':

        SORTING_METHODS = ['id', 'time', 'bumpCount']

        sort = req.args.get('sort')
        num = req.args.get('num')
        thread = req.args.get('thread')
        offset = req.args.get('offset')

        # Validate sort
        if not sort:
            sort = SORTING_METHODS[0]

        if sort not in SORTING_METHODS:
            reject_request("Invalid sorting method")
		
        # validate offset
        try:
            offset = int(offset)
        except:
            reject_request("Offset should be an integer")
        if not offset:
            offset = 0

        # validate num
        try:
            num = int(num)
        except:
            reject_request("Num should be an integer")

        if not num:
            num = 50

        if num > 1000:
            reject_request("Fetch limit 1000")

        # Validate thread
        if not post_exists(db, board, thread):
            reject_request('The thread you are replying to does not exist')

        # execute query
        if (type(thread) is not int) and thread:
            reject_request('Thread must be of type int')

        if thread:
            data = db.execute('select * from {} where replyTo=? or id=? order by id desc limit ? offset ?'.format(board),
                                (thread, thread, num, offset)).fetchall()

        else:
            data = db.execute('select * from {} order by id desc limit ? offset ?'.format(board), (num, offset)).fetchall()

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
