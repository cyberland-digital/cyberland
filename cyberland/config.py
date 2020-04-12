import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Enable Flask debug mode
DEBUG = True

# Database connection string
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
