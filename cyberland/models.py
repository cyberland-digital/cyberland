from .app import db

# setup model classes for the ORM here


class Board(db.Model):
    __tablename__ = 'boards'

    id = db.Column('board_id', db.Integer, primary_key=True)
    name = db.Column('board_name', db.String(20))
    slug = db.Column(db.String(1))

    def __init__(self, name, slug):
        self.name = name
        self.slug = slug


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column('post_id', db.Integer, primary_key=True)
    content = db.Column('post_content', db.String(10000))
    reply_to = db.Column('reply_to', db.ForeignKey('posts.post_id'), nullable=True)
    board = db.Column('board', db.Integer, db.ForeignKey('boards.board_id'))

    def __init__(self, content, reply_to=None):
        self.content = content
        self.reply_to = reply_to
