from __future__ import print_function

import random, string

from flask import Blueprint, redirect, url_for, flash, render_template
from config import Config
from flask_login import current_user, login_user
from app.Controller.auth_forms import RegistrationForm, LoginForm
from app.Model.models import User
from app import db

bp_auth = Blueprint('auth', __name__)
bp_auth.template_folder = Config.TEMPLATE_FOLDER

@bp_auth.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    rform = RegistrationForm()
    if rform.validate_on_submit():
        user = User(username = rform.username.data, first_name = rform.first_name.data, last_name = rform.last_name.data, email = rform.email.data)
        user.set_password(rform.password.data)
        ver = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        user.set_verification(ver)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations! You are now a registered user. Your verification code is: {} Please save this somewhere!'.format(ver))
        return redirect(url_for('routes.index'))
    return render_template('register.html', form = rform)

@bp_auth.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    lform = LoginForm()
    if lform.validate_on_submit():
        user = User.query.filter_by(username = lform.username.data).first()
        if (user is None) or (user.get_password(lform.password.data) == False):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember = lform.remember_me.data)
        return redirect(url_for('routes.index'))
    return render_template('login.html', form = lform)