from __future__ import print_function

import sys

from flask import Blueprint, render_template, flash, redirect, url_for, request
from config import Config
from flask_login import login_required, current_user
from flask import current_app as app

from app import db
from app.Model.models import User, Post, Comment
from app.Controller.forms import PostForm, CommentForm

bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER

@bp_routes.route('/', methods=['GET'])
@bp_routes.route('/index',methods=['GET'])
@login_required
def index():
    posts = Post.query.filter_by(user_id = current_user.id).order_by(Post.post_datetime.desc())
    return render_template('index.html', posts_query = posts)

@bp_routes.route('/post',methods=['GET','POST'])
@login_required
def post():
    pform = PostForm()
    if pform.validate_on_submit():
        thepost = Post(title = pform.title.data, body = pform.body.data, user_id = current_user.id)
        db.session.add(thepost)
        db.session.commit()
        flash("New blog post has been created!")
        return redirect(url_for('routes.index'))
    return render_template('create_post.html', form = pform)

@bp_routes.route('/delete_post/<post_id>', methods=['GET','POST'])
@login_required
def delete_post(post_id):
    thepost = Post.query.filter_by(id = post_id).first()
    if (thepost is None):
        flash("Post does not exist")
        return redirect(url_for('routes.index'))
    if (thepost.user_id != current_user.id):
        flash("This post does not belong to you!")
        return redirect(url_for('routes.index'))
    db.session.delete(thepost)
    db.session.commit()
    flash('The post has been succesfully deleted!')
    return redirect(url_for('routes.index'))

@bp_routes.route('/profile/<user_id>', methods=['GET'])
@login_required
def view_profile(user_id):
    theuser = User.query.filter_by(id = user_id).first()
    if theuser is None:
        flash('User does not exist!')
        return redirect(url_for('routes.index'))
    return render_template('profile.html', the_user = theuser)

@bp_routes.route('/comment/<post_id>', methods=['GET','POST'])
@login_required
def comment(post_id):
    thepost = Post.query.filter_by(id = post_id).first()
    if thepost is None:
        flash('Post does not exist!')
        return redirect(url_for('routes.index'))
    cform = CommentForm()
    if cform.validate_on_submit():
        thecomment = Comment(body = cform.body.data, post_id = thepost.id, user_id = current_user.id)
        db.session.add(thecomment)
        db.session.commit()
        flash('Comment created successfully')
        return redirect(url_for('routes.index'))
    return render_template('create_comment.html', form=cform, post=thepost)

@bp_routes.route('/comments/<post_id>', methods=['GET','POST'])
@login_required
def comments(post_id):
    thepost = Post.query.filter_by(id = post_id).first()
    if thepost is None:
        flash('Post does not exist!')
        return redirect(url_for('routes.index'))
    cform = CommentForm()
    if cform.validate_on_submit():
        thecomment = Comment(body = cform.body.data, post_id = thepost.id, user_id = current_user.id)
        db.session.add(thecomment)
        db.session.commit()
        flash('Comment created successfully')
        return redirect(url_for('routes.comments',post_id=thepost.id))
    return render_template('comments.html', form=cform, post=thepost)