# import flask
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# berikan nama module flask
flasko = Flask(__name__)
flasko.config.from_object(Config)
db = SQLAlchemy(flasko)
migrate = Migrate(flasko, db)
login = LoginManager(flasko)
login.login_view = 'login'

# import route
from app import routes, models
