"""
The flask application package.
"""
import logging
import sys
import msal
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session

app = Flask(__name__)
app.config.from_object(Config)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
msal_app = msal.ConfidentialClientApplication(
	client_id=app.config.get("CLIENT_ID"),
	client_credential=app.config.get("CLIENT_SECRET"),
	authority="https://login.microsoftonline.com/common",
)
Session(app)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = 'login'

import FlaskWebProject.views
