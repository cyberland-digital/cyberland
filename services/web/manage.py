from flask.cli import FlaskGroup
from flaskr import create_app, db
from flaskr.models import BoardsModel

app = create_app()
cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()

    boards = [
        BoardsModel('technology', 't'),
        BoardsModel('off-topic', 'o'),
        BoardsModel('news', 'n'),
        BoardsModel('images', 'i'),
        BoardsModel('client-test', 'c')
    ]

    for board in boards:
        db.session.add(board)
    try:
        db.session.commit()
        print("changes commited to database successfully")
    except:
        print("error commiting changes to database")


if __name__ == '__main__':
    cli()
