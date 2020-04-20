from flaskr import db
from datetime import datetime


class BoardsModel(db.Model):
    __tablename__ = 'boards'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True)
    slug = db.Column(db.String(2), unique=True)
    character_limit = db.Column(db.Integer, default=1000)
    federated = db.Column(db.Boolean, default=False)

    def __init__(self, name, slug, character_limit=1000, federated=False):
        self.name = name
        self.slug = slug
        self.character_limit = character_limit
        self.federated = federated

    def __repr__(self):
        return f"<Board /{self.slug}/>"


class PostsModel(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    board = db.Column(db.Integer, db.ForeignKey(BoardsModel.id), nullable=False)

    content = db.Column(db.Text, nullable=False)

    bumps = db.Column(db.Integer, default=0, nullable=False)
    replyTo = db.Column(db.Integer, default=0, nullable=False)

    archived = db.Column(db.Boolean, default=False)
    time = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def __init__(self, board, content, replyTo):
        self.board = board
        self.content = content
        self.replyTo = replyTo

    def __repr__(self):
        return f"<Post bumps:{self.bumps} thread:{self.replyTo}>"
