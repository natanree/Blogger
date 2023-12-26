from app import db, login

from flask_login import UserMixin
from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
class User(db.Model, UserMixin):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    verification_hash = db.Column(db.String(10))
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(128))
    join_date = db.Column(db.Date, default = date.today)
    posts = db.Relationship('Post', backref='poster', lazy='dynamic')
    comments = db.Relationship('Comment', backref='commenter', lazy='dynamic')

    def __repr__(self):
        return '<User {} - {}'.format(self.id,self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def set_verification(self, verification):
        self.verification_hash = generate_password_hash(verification)
    
    def get_verification(self, verification):
        return check_password_hash(self.verification_hash, verification)
    
class Post(db.Model):
    __tablename__='post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.String(1000))
    post_datetime = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.Relationship('Comment', backref='post', lazy='dynamic')

class Comment(db.Model):
    __tablename__='comment'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(1000))
    post_datetime = db.Column(db.DateTime, default = datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))