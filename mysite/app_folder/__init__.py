from flask import Flask
from site_config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.ext.cache import Cache


app_run = Flask(__name__)

cache = Cache(app_run, config={'CACHE_TYPE': 'simple'})

app_run.config.from_object(Config)
db = SQLAlchemy(app_run)
migrate = Migrate(app_run, db)
# toolbar = DebugToolbarExtension(app_run)

from app_folder import routes, models
