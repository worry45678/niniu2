from flask import render_template, session, redirect, url_for, request, jsonify
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
    session['seat'] = room.userpos(current_user)
    return redirect(url_for('.room'))

@main.route('/joinRoom',methods=['POST'])
def joinRoom():
    if Room.query.filter_by(id=request.form.get('room')).first():
        room = Room.query.filter_by(id=request.form.get('room')).first()
        session['room'] = room.id
        if room.userpos(current_user) == 0 and room.count() < 5:
            room.join(current_user)
            db.session.add(room)
            db.session.commit()
            session['seat'] = room.userpos(current_user)
            return redirect(url_for('.room'))
        elif room.userpos(current_user) != 0:
            session['seat'] = room.userpos(current_user)
            return redirect(url_for('.room'))
    return 'join failed'

@main.route('/room')
def room():
    if session.get('room'):
        return render_template('room.html', user=current_user.name, room=session['room'])
    else:
        return redirect(url_for('.index'))

@main.route('/status')
def status():
    room = Room.query.filter_by(id=session['room']).first()
    return jsonify(room.getStatus(current_user))

@main.route('/test')
def test():
    return render_template('test.html')