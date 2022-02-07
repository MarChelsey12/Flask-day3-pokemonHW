from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# init
app = Flask(__name__)
#link config to the app
app.config.from_object(Config)

#init my login manager
login = LoginManager(app)
# this is where you are sent if you're not logged in
login.login_view = 'login'

# do inits for database stuff
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models