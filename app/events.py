from flask import session
from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from . import socketio
from datetime import datetime

@socketio.on('joined', namespace='/game')
def joined(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'user': current_user.name,'room':room,'action':'join','time':datetime.utcnow().strftime('%Y-%d-%m %H:%M:%S')}, room=room)

@socketio.on('message', namespace='/game')
def mess(message):
    room = session.get('room')
    emit('message', {'user': current_user.name,'msg':message['msg'], 'room':room,'action':'*action*','time':datetime.utcnow().strftime('%Y-%d-%m %H:%M:%S')}, room=room)

@socketio.on('action', namespace='/game')
def action(message):
    room = session.get('room')
    emit('action', {'user': current_user.name,'room':room,'action':'*action*','time':datetime.utcnow().strftime('%Y-%d-%m %H:%M:%S')}, room=room)