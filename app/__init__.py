from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

from app import signup, token, login, models