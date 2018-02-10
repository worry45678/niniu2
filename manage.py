import os
from app import create_app, db, socketio
from app.models import User, Role, Room, Paiju
from flask_script import Manager, Shell


app = create_app(os.getenv('PYTHON_CONFIG') or 'default')
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Room=Room, Paiju=Paiju)

manager.add_command('shell', Shell(make_context=make_shell_context))

if __name__ == '__main__':
    #manager.run()
    socketio.run(app)