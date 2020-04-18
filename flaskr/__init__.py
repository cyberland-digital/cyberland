from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flaskr.utils import send_json
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

VERSION_STRING = 'V1.0'

db = SQLAlchemy()
limiter = Limiter()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": "*"}})

    app.config.from_object("../config.Config")

    @app.errorhandler(404)
    def not_found_error(error):
        return send_json({'error': "path not found"}, status=404)

    @app.errorhandler(500)
    def server_error(error):
        return send_json({'error': "server error"})

    from . import db
    db.init_app(app)

    from . import limiter
    limiter.init_app(app)

    from . import migrate
    migrate.init_app(app, db)

    from . import post
    app.register_blueprint(post.bp)

    return app
