import os
from app import create_app, db, socketio
from app.models import User, Role, Room, Paiju
from flask_script import Manager, Shell


app = create_app(os.getenv('PYTHON_CONFIG') or 'default')

if __name__ == '__main__':
    #manager.run()
    socketio.run(app)