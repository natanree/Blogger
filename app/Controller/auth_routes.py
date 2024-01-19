from __future__ import print_function

import random, string

from flask import Blueprint, redirect, url_for, flash, render_template, request
from config import Config
from flask_login import current_user, login_user, login_required, logout_user
from app.Controller.auth_forms import RegistrationForm, LoginForm, EditProfileForm
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
        for tag in rform.tags.data:
            user.preferred_tags.append(tag)
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

@bp_auth.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.index'))

@bp_auth.route('/edit_profile/<user_id>', methods=['GET','POST'])
@login_required
def edit_profile(user_id):
    user = User.query.filter_by(id = user_id).first()
    if user is None:
        flash('User does not exist!')
        return redirect(url_for('routes.index'))
    if current_user.id != user.id:
        flash('You cannot edit profile\'s that are not yours!')
        return redirect(url_for('routes.index'))
    eform = EditProfileForm()
    if eform.validate_on_submit():
        if (user.get_password(eform.password.data)==False):
            flash('Invalid password')
            return redirect(url_for('auth.edit_profile', user_id=user.id))
        if (eform.new_password.data != ""):
            user.set_password(eform.new_password.data)
        user.first_name = eform.first_name.data
        user.last_name = eform.last_name.data
        user.email = eform.email.data
        user.username = eform.username.data
        for tag in user.preferred_tags:
            user.preferred_tags.remove(tag)
        for tag in eform.tags.data:
            user.preferred_tags.append(tag)
        db.session.commit()
        flash('Your changes have been saved!')
        return redirect(url_for('routes.view_profile',user_id=user.id))
    elif request.method == 'GET':
        eform.username.data = user.username
        eform.first_name.data = user.first_name
        eform.last_name.data = user.last_name
        eform.email.data = user.email
        for tag in user.preferred_tags:
            eform.tags.data.append(tag)
        
    return render_template('edit_profile.html', form=eform)