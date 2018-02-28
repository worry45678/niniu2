from flask import session
from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from . import socketio, db
from datetime import datetime
import json, random, math
from .models import Room, Paiju, calcmark

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
    elif message['action'] == 'qiangzhuang':
        # 是否抢庄的数据保存到paiju.zhuang字段中
        if message['content'] == 1:
            paiju = Paiju.query.filter_by(room_id=room.id).filter_by(finish=0).first()
            pos = 2 ** (session['seat']-1)
            paiju.zhuang = paiju.zhuang | pos
            db.session.add(paiju)
            db.session.commit()
            re = {'user': current_user.name,'seat':session['seat'], 'action':'qiangzhuang', 'error':'ok', 'content':message['content'], 'time':datetime.utcnow().strftime('%Y-%d-%m %H:%M:%S')}
            emit('action', re, room=room.id)
    elif message['action'] == 'choicezhuang':
        # 抢庄选择完毕，选择庄家
        paiju = Paiju.query.filter_by(room_id=room.id).filter_by(finish=0).first()
        pos = 2 ** (session['seat']-1)
        if message['content'] == 1:
            paiju.zhuang = paiju.zhuang | pos
        y = [i for i in [paiju.zhuang & int(2**(i)) for i in range(5)] if i>0]
        paiju.zhuang = math.log(random.choice(y))/math.log(2) + 1
        db.session.add(paiju)
        db.session.commit()
        re = {'user': current_user.name,'seat':session['seat'], 'action':'choicezhuang', 'error':'ok', 'content':[message['content'],paiju.zhuang], 'time':datetime.utcnow().strftime('%Y-%d-%m %H:%M:%S')}
        emit('action', re, room=room.id)
    elif message['action'] == 'xiazhu':
        paiju = Paiju.query.filter_by(room_id=room.id).filter_by(finish=0).first()
        paiju.xiazhu(session['seat'],message['content'])
        re = {'user': current_user.name,'seat':session['seat'], 'action':message['action'], 'error':'ok', 'content': message['content'], 'time':datetime.utcnow().strftime('%Y-%d-%m %H:%M:%S')}
        emit('action',re,room=room.id)
    elif message['action'] == 'fapai2':
        # 完整发牌，应加入验证是否所有人都已经下注的验证
        paiju = Paiju.query.filter_by(room_id=room.id).filter_by(finish=0).first()
        if paiju.checkxiazhu and paiju.status != 'show':
            calcmark(paiju)
            print('calc--------------------------------')
            paiju.status = 'show'
            db.session.add(paiju)
            db.session.commit()
        pai = json.loads(paiju.paixu)
        re = {'user': current_user.name,'seat':session['seat'], 'action':message['action'], 'error':'ok', 'content':pai[session['seat']-1][4], 'time':datetime.utcnow().strftime('%Y-%d-%m %H:%M:%S')}
        emit('action', re)
    elif message['action'] == 'show':
        re = {'user': current_user.name,'seat':session['seat'], 'action':message['action'], 'error':'ok', 'content':message['content'], 'time':datetime.utcnow().strftime('%Y-%d-%m %H:%M:%S')}
        emit('action', re, room=room.id)
    elif message['action'] == 'finish':
        # 可以考虑加入对牌局的验证
        paiju = Paiju.query.filter_by(room_id=room.id).filter_by(finish=0).first()
        re = {'user': current_user.name,'seat':session['seat'], 'action':message['action'], 'error':'ok', 'content':message['content'],'marks':paiju.marks(), 'time':datetime.utcnow().strftime('%Y-%d-%m %H:%M:%S')}
        paiju.finish = 1
        db.session.add(paiju)
        db.session.commit()
        emit('action', re, room=room.id)
    else:
        re = {'user': current_user.name,'seat':session['seat'], 'action':message['action'], 'error':'ok', 'content':message['content'], 'time':datetime.utcnow().strftime('%Y-%d-%m %H:%M:%S')}
        emit('action', re, room=room.id)