from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import hiddendata
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = hiddendata.SECRET
app.config['SQLALCHEMY_DATABASE_URI'] = hiddendata.DB_CON_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


from MisterMasticate import route
