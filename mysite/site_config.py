import os
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'd3app.db')
    DEBUG = True

