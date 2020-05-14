from flask import Blueprint, request, abort
from flaskr.models import BoardsModel, PostsModel
from flaskr.utils import send_json, send_text_template, send_json_error, check_newlines
from flaskr import db, limiter

bp = Blueprint('post', __name__)


# Tutorial and basic documentation routes


@bp.route('/', methods=['GET'])
def index():
    return send_text_template("index.txt")


@bp.route("/tut.txt", methods=['GET'])
def tut():
    return send_text_template("tut.txt")


# text board logic


@bp.route("/<string:board>/", methods=['POST'])
@limiter.limit('2 per minute')
@limiter.limit("1 per 10 seconds")
def create_post(board):
    board = BoardsModel.query.filter_by(slug=board).first()
    if not board:
        return abort(404)

    content = request.form.get('content')
    replyTo = request.form.get('replyTo')
    # Validation

    # condition: replyTo must be an integer if specified
    if replyTo:
        try:
            replyTo = int(replyTo)
        except ValueError:
            return send_json_error("'replyTo' must be an integer")

    # condition: must have content
    if not content:
        return send_json_error("'content' must be present")

    # condition: post content must be a string
    if type(content) is not str:
        return send_json_error("'content' must be a string")

    # condition: post content must have a length greater than 1
    if len(content) < 1:
        return send_json_error("'content' must be longer than 1 character")

    # condition: check content length with board character limit
    char_limit = board.character_limit
    if len(content) > char_limit:
        return send_json_error(f"'content' is too long for the requested board MAX LENGTH: {char_limit}")

    # check the concentration of newlines in a message
    if not check_newlines(content):
        return send_json_error("'content' has too many newlines for the number of characters present")

    # replyTo VALIDATION
    # If post is replying to another post (not OP) check existence
    if replyTo:
        reply = PostsModel.query.filter_by(id=replyTo, board=board.id).first()
        if reply:
            new_post = PostsModel(board=board.id, content=content, replyTo=reply.id)
            reply.bumps += 1
        else:
            return send_json_error("'replyTo' does not exist in database", status=404)

    else:
        new_post = PostsModel(board=board.id, content=content, replyTo=0)

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
@limiter.limit('30 per minute')
@limiter.limit("1 per second")
def get_posts(board):
    board = BoardsModel.query.filter_by(slug=board).first()
    if not board:
        return abort(404)

    num = request.args.get('num')
    offset = request.args.get('offset')
    thread = request.args.get('thread')

    # Validate parameters
    if thread:
        try:
            thread = int(thread)
        except ValueError:
            return send_json_error("'thread' must be a integer")
        if thread < 0:
            return send_json_error("'thread' must not be negative")

    if offset:
        try:
            offset = int(offset)
        except ValueError:
            return send_json_error("'offset' must be a integer")
        if offset < 0:
            return send_json_error("'offset' must not be negative")

    if num:
        try:
            num = int(num)
        except ValueError:
            return send_json_error("'num' must be a integer")
        if num < 0:
            return send_json_error("'num' must not be negative")

    # query database
    if thread or thread == 0:
        posts = PostsModel.query.filter_by(board=board.id, replyTo=thread).order_by(PostsModel.id.desc()).offset(
            offset).limit(num).all()
    else:
        posts = PostsModel.query.filter_by(board=board.id).order_by(PostsModel.id.desc()).offset(offset).limit(
            200).all()

    results = [{
        "id": post.id,
        "content": post.content,
        "replyTo": post.replyTo,
        "bumpCount": post.bumps,
        "time": post.time
    } for post in posts]

    return send_json(results)
