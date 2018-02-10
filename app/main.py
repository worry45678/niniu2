from flask import render_template, session, redirect, url_for, request
from flask_login import current_user
from flask import Blueprint
from .models import Room
from . import db
import json


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/createRoom')
def createRoom():
    room = Room(user1_id=current_user.id)
    db.session.add(room)
    db.session.commit()
    session['room'] = room.id
    return json.dumps(room.id)

@main.route('/joinRoom')
def joinRoom():
    if Room.query.filter_by(id=request.args.get('roomid')).first():
        room = Room.query.filter_by(id=request.args.get('roomid')).first()
        session['room'] = room.id
        if room.userpos(current_user) == 0 and room.count < 5:
            room.join(current_user)
        db.session.add(room)
        db.session.commit()
        return 'joinroom'
    else:
        return 'join failed'