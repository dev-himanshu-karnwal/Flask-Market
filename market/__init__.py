'''__init__ file for market module'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# creating flask application
app = Flask(__name__)
# configure db link
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
# secret key for forms
app.config['SECRET_KEY'] = 'c27b077692ae21bd40518b20'

# create db object for performing operations
db = SQLAlchemy(app)
# used for password hashing and matching
bcrypt = Bcrypt(app)
# manage user login, logout, etc.
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'


# import routes
def imp():
    from market import routes


imp()
