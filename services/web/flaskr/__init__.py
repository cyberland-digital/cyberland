from flask_limiter import Limiter
from .utils import send_json_error
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

    app.config.from_object("flaskr.config.Config")

    # handle errors. always send json response

    @app.errorhandler(500)
    def server_error(error):
        return send_json_error("server error", status=500)

    @app.errorhandler(429)
    def slow_down(error):
        return send_json_error("Too many requests, slow down", status=429)

    # configure middleware
    from . import db, limiter, migrate, post
    db.init_app(app)
    limiter.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(post.bp)

    return app
