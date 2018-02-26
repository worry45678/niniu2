from flask import session
from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from . import socketio
from datetime import datetime
import json
from .models import Room, Paiju

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
    room = Room.query.filter_by(id=session.get('room')).first()
    if message['action']  == 'fapai':
        if Paiju.query.filter_by(room_id=room.id).first() is None:
            Paiju.generate_paiju(room.id)
        paiju = Paiju.query.filter_by(room_id=room.id).filter_by(finish=0).first()
        pai = json.loads(paiju.paixu)
        re = {'user': current_user.name,'seat':session['seat'], 'action':message['action'], 'error':'ok', 'content':pai[session['seat']-1][0:4], 'time':datetime.utcnow().strftime('%Y-%d-%m %H:%M:%S')}
        emit('action', re)
    else:
        re = {'user': current_user.name,'seat':session['seat'], 'action':message['action'], 'error':'ok', 'content':message['content'], 'time':datetime.utcnow().strftime('%Y-%d-%m %H:%M:%S')}
        emit('action', re, room=room.id)