from flask import session
from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from . import socketio

def joinroom(room):
    join_room(room)
    emit('status',{'msg':current_user.name + 'has entered the room'})

@socketio.on('joined', namespace='/game')
def joined(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': current_user.name + 'has entered this room'}, room=room)

@socketio.on('message', namespace='/game')
def mess(message):
    room = session.get('room')
    print('*************************',message)
    emit('message', {'msg':'message'}, room=room)