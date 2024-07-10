# views.py
from flask import Blueprint, render_template, request, redirect, url_for
from .models import db, Post, Comment, Tag, User
from . import login_manager  # 假设 login_manager 在 __init__.py 中初始化
from flask_login import login_user, login_required, current_user, logout_user
from datetime import datetime
import pytz
main = Blueprint('main', __name__)
# 登录管理器的用户加载函数
@login_manager.user_loader
def load_user(user_id):
    try:
        # 尝试将 user_id 转换为整数，如果成功，说明不是 'admin'
        user_id = int(user_id)
        return User.query.get(user_id)
    except ValueError:
        # 如果转换失败，说明可能是 'admin'
        if user_id == 'admin':
            # 创建一个具有管理员属性的用户对象
            admin_user = User()
            admin_user.id = 'admin'
            # 这里可以设置其他管理员特有的属性
            return admin_user
        # 如果不是 'admin'，返回 None
        return None
# 路由：登录管理员
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        #is_admin = request.form.get('is_admin') == 'on'
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            if user.is_admin:  # 判断用户是否为管理员
                return redirect(url_for('admin.index')) 
            else:
                return redirect(url_for('main.index'))  # 普通用户登录后的界面
        else:
            print("Password check failed")
    return render_template('login.html')

# 路由：注销管理员
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# 路由：首页
@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        # 如果用户已经登录，显示博客内容
        posts = Post.query.order_by(Post.created_at.desc()).all()

        
        for post in posts:
            post.comments_html = ''.join([render_comment_html(comment, post.id) for comment in post.comments if comment.parent is None])
        return render_template('index.html', posts=posts)
    # 如果用户未登录，显示登录界面
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.index'))
    return render_template('login.html')
    
# @main.route('/posts')
# @login_required
# def post_page():
#     posts = Post.query.all()
#     print("Rendering post_page with posts", posts)
#     return render_template('index.html', posts=posts)

# 路由：为指定的 Post 添加标签
@main.route('/add_tag/<int:post_id>', methods=['GET', 'POST'])
def add_tag(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        tag_name = request.form['tag_name']
        # 创建新的 Tag，并将 post_id 设置为现有 Post 的 id
        new_tag = Tag(name=tag_name, post_id=post.id, user_id=current_user.id)
        db.session.add(new_tag)
        db.session.commit()
        return redirect(url_for('main.index'))   
    return render_template('add_tag.html', post=post)

# 路由：为指定的 Post 添加评论
@main.route('/add_comment/<int:post_id>', methods=['GET', 'POST'])
@main.route('/add_comment/<int:post_id>/<int:parent_id>', methods=['GET', 'POST'])
def add_comment(post_id, parent_id=None):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        comment_content = request.form['comment_content']
        new_comment = Comment(content=comment_content, post_id=post.id, user_id=current_user.id, parent_id=parent_id,timestamp=datetime.utcnow())
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('add_comment.html', post=post, parent_id=parent_id)

def render_comment_html(comment, post_id, level=0):
    username = "Unknown User" if comment.user is None else comment.user.username
    reply_link = f'<a href="/add_comment/{post_id}/{comment.id}">Reply</a>'
    toggle_replies_link = f'<button onclick="toggleReplies(\'replies-{comment.id}\')">Toggle Replies</button>'
    if comment.timestamp:
        utc_timestamp = comment.timestamp.replace(tzinfo=pytz.utc)
        # 转换为北京时间
        beijing_time = utc_timestamp.astimezone(pytz.timezone('Asia/Shanghai'))
        formatted_time = beijing_time.strftime('%Y-%m-%d %H:%M:%S')
    else:
        formatted_time = "Time not available"

    html = '<li>' + \
           f'<div class="comment" style="margin-left: {level * 20}px;">' + \
           f'{comment.content} by {username} at {formatted_time} {reply_link} {toggle_replies_link}</div>'

    if comment.replies:
        html += f'<ul id="replies-{comment.id}" class="comment-reply hide">'
        for reply in comment.replies:
            html += render_comment_html(reply, post_id, level + 1)
        html += '</ul>'
    html += '</li>'

    return html


