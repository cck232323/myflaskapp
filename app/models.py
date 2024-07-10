from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from . import db
from datetime import datetime

login_manager = LoginManager()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128))  # 密码明文存储
    is_admin = db.Column(db.Boolean, default=False)  # 新增字段，标识是否为管理员

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))  # 图片 URL
    tags = db.relationship('Tag', backref='post', lazy=True)
    comments = db.relationship('Comment', backref='post', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 
class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# 定义评论模型,并且需要对评论进行评论
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

