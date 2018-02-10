from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
import json

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        data = json.loads(request.data)
        user = User.query.filter_by(name=data.get('username')).first()
        if user is not None and user.verify_password(data.get('password')):
            login_user(user)
            return 'login'
        else:
            return 'wrong password',400
    return render_template('index.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return 'logout'