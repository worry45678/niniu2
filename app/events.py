from flask import session
from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from . import socketio
from datetime import datetime

@socketio.on('joined', namespace='/game')
def joined(message):
    room = session.get('room')
    join_room(room)
    emit('action', {'user': current_user.name, 'seat':session['seat'], 'action':'join', 'error':'ok', 'content':None, 'time':datetime.utcnow().strftime('%Y-%d-%m %H:%M:%S')}, room=room)


@socketio.on('message', namespace='/game')
def mess(message):
    room = session.get('room')
    emit('message', {'user': current_user.name,'msg':message['msg'], 'room':room,'time':datetime.utcnow().strftime('%Y-%d-%m %H:%M:%S')}, room=room)

@socketio.on('action', namespace='/game')
def action(message):
    room = session.get('room')
    if message['action'] == 'fapai':
        print('fapai')

    re = {'user': current_user.name,'seat':session['seat'], 'action':message['action'], 'error':'ok', 'content':message['content'], 'time':datetime.utcnow().strftime('%Y-%d-%m %H:%M:%S')}
    emit('action', re, room=room)