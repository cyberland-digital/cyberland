from flask import Flask, render_template, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from cyberland.models import *

# App config
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)







if __name__ == '__main__':
    app.run()
