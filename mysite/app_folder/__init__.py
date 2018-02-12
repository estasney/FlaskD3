from flask import Flask
from site_config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app_run = Flask(__name__)
app_run.config.from_object(Config)
db = SQLAlchemy(app_run)
migrate = Migrate(app_run, db)
# toolbar = DebugToolbarExtension(app_run)

from app_folder import routes, models

# Does this re