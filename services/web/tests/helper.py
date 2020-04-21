from flaskr import db
from flaskr.models import BoardsModel, PostsModel

def create_board(name, slug, character_limit, federated):
    new_board = BoardsModel(name=name, slug=slug, character_limit=character_limit, federated=federated)
