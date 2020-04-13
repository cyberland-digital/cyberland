import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.errorhandler(404)
    def not_found_error(error):
        return 'Page not found', 404

    from . import db
    db.init_app(app)

    from . import post

    limiter = Limiter(app, key_func=get_remote_address, default_limits=["1/second"])
    limiter.limit("5/minute", methods=['POST'])(post.bp)
    limiter.limit("1/second")(post.bp)

    app.register_blueprint(post.bp)

    return app
