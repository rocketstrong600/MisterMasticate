from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import hiddendata
import os

cloud_sql_connection_name = os.environ.get("CLOUD_SQL_CONNECTION_NAME")

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CON_URL
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


from MisterMasticate import route
