from flask import Blueprint
from flaskr.models import BoardsModel, PostsModel
from flaskr.utils import send_json, send_text_template, send_json_error
from flaskr import db
from flask_request_validator import (
    PATH,
    FORM,
    GET,
    Param,
    Pattern,
    validate_params,
    MaxLength,
    MinLength
)

bp = Blueprint('post', __name__)


@bp.route('/')
def index():
    return send_text_template("index.txt")


@bp.route("/tut.txt")
def tut():
    return send_text_template("tut.txt")


# board logic
# TODO: add redirects from /x to /x/


@bp.route("/<string:board>/", methods=['POST'])
@validate_params(
    Param('board', PATH, str, required=True, rules=[MaxLength(1), MinLength(1)]),
    Param('content', FORM, str, required=True, rules=[MinLength(1)]),
    Param('replyTo', FORM, int, required=False, default=0)
)
def create_post(board, content, replyTo):
    board = BoardsModel.query.filter_by(slug=board).first()
    if not board:
        return send_json_error("Board not found in database", status=404)

    # If post is replying to another post (not OP) check existence
    if replyTo != 0:
        reply = PostsModel.query.filter_by(id=replyTo, board=board).first()
        if reply:
            new_post = PostsModel(board, content, reply.id)
            reply.bumps += 1
        else:
            return send_json_error("The post you are replying to does not exist", status=404)

    elif replyTo == 0:
        new_post = PostsModel(board, content, replyTo)
    else:
        return send_json_error("There was a problem with your request")

    db.session.add(new_post)
    db.session.commit()
    result = {
        "id": new_post.id,
        "content": new_post.content,
        "replyTo": new_post.replyTo,
        "bumpCount": new_post.bumps,
        "time": new_post.time
    }
    return send_json(result, status=201)


@bp.route("/<string:board>/", methods=['GET'])
@validate_params(
    Param('board', PATH, str, required=True, rules=[MaxLength(1), MinLength(1)]),
    Param('num', GET, str, required=False),
    Param('offset', GET, int, required=False, default=0)
)
def get_posts(board, num, offset, thread):
    board = BoardsModel.query.filter_by(slug=board).first()
    if not board:
        return send_json_error("Board not found in database", status=404)

    # Get posts from the database
    posts = PostsModel.query.filter_by(board=board).all()
