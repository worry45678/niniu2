from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_socketio import SocketIO

socketio = SocketIO()

db = SQLAlchemy()
login_manger = LoginManager()
login_manger.session_protection = 'basic'
login_manger.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manger.init_app(app)
    socketio.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from . import events

    return app
