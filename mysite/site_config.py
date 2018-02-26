import os
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'd3appv3.db')
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

