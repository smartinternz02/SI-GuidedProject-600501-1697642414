from flask import Flask
# import tensorflow
# from tensorflow import keras
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager



app = Flask(__name__)


app.config['SECRET_KEY']='4513a7e2ae1f40856f51a864c640f65d447390'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.site'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager =LoginManager(app) 
login_manager.login_view='login'
login_manager.login_message_category='info'

from detection import routes
