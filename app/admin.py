from flask_admin import Admin,AdminIndexView,expose
from flask_admin.contrib.sqla import ModelView
from .models import db, Post, Tag, Comment
from flask import redirect, url_for, request, current_app
from flask_login import current_user
from flask_admin.model.template import macro
from flask_admin import expose
from datetime import datetime
import pytz
import os
from werkzeug.utils import secure_filename
# 在 admin.py 中
from . import photos
def format_datetime(view, context, model, name):
    utc_time = getattr(model, name)
    if utc_time:
        beijing_time = utc_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Shanghai'))
        return beijing_time.strftime('%Y-%m-%d %H:%M:%S')
    return ''

class MyAdminHomeView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    @expose('/')
    def index(self):
        if not self.is_accessible():
            # 如果用户没有权限访问，重定向到登录页面
            return redirect(url_for('main.login'))
        # 渲染 Flask-Admin 的后台主页模板
        return self.render('admin/my_home.html')

# class MyAdminHomeView(AdminIndexView):
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.is_admin
#     @expose('/')
#     def index(self):
#         return redirect(url_for('templates/admin/my_home.html'))
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    column_formatters = {
        'created_at': format_datetime
    }
    @expose('/new/', methods=('GET', 'POST'))
    # def create_view(self):
    #     print(current_app.extensions)
    #     if request.method == 'POST' and 'image' in request.files:
            
    #         # photos = current_app.extensions['photos']  # 获取 photos
    #         # photos = UploadSet('photos', IMAGES)
    #         filename = photos.save(request.files['image'])
    #         image_url = photos.url(filename)
    #         beijing_tz = pytz.timezone('Asia/Shanghai')
    #         created_at = datetime.now(tz=pytz.utc).astimezone(beijing_tz)
            
    #         new_post = Post(title=request.form['title'],
    #                         content=request.form['content'],
    #                         author=request.form['author'],
    #                         image_url=image_url,
    #                         created_at=created_at
    #                         )
    #         db.session.add(new_post)
    #         db.session.commit()
    #         return redirect(url_for('.index_view'))
    #     return self.render('create_post.html')
    def create_view(self):
            if request.method == 'POST' and 'image' in request.files:
                file = request.files['image']
                if file:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], filename)
                    
                    if not os.path.exists(file_path):
                        photos.save(file, name=filename)
                    
                    image_url = photos.url(filename)
                    beijing_tz = pytz.timezone('Asia/Shanghai')
                    created_at = datetime.now(tz=pytz.utc).astimezone(beijing_tz)
                    
                    new_post = Post(title=request.form['title'],
                                    content=request.form['content'],
                                    author=request.form['author'],
                                    image_url=image_url,
                                    created_at=created_at)
                    db.session.add(new_post)
                    db.session.commit()
                    return redirect(url_for('.index_view'))
            return self.render('create_post.html')

class TagModelView(ModelView):
    column_formatters ={'timestamp': format_datetime}
    column_list = ('name', 'post_id', 'user.username', 'timestamp')
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        if request.method == 'POST':
            tag_name = request.form['name']
            post_id = request.form['post_id']
            new_tag = Tag(name=tag_name, post_id=post_id, user_id=current_user.id)
            db.session.add(new_tag)
            db.session.commit()
            return redirect(url_for('admin.index'))
        else:
        # 从请求的查询参数中获取 post_id
            posts = Post.query.all()
            # 将 post_id 传递到模板
            return self.render('create_tag.html', posts=posts)
        
    
class CommentModelView(ModelView):
    
    column_formatters = {
        'replies': macro('render_replies'),
        'parent_user': lambda v, c, m, p: m.parent.user.username if m.parent else ''
    }
    column_list = ('content', 'post_id', 'user.username', 'parent_user','timestamp')
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin
    
    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        if request.method == 'POST':
            comment_content = request.form['content']
            post_id = request.form['post_id']
            new_comment = Comment(content=comment_content, post_id=post_id, user_id=current_user.id)
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for('admin.index'))
        else:
            posts = Post.query.all()
            return self.render('create_comment.html',posts=posts)
        
    
def init_admin(app):
    admin_home_view = MyAdminHomeView(name='Home', template='admin/my_home.html', url='/admin')
    admin = Admin(app, name='MyBlog',index_view= admin_home_view,template_mode='bootstrap3')
    admin.add_view(MyModelView(Post, db.session))
    admin.add_view(TagModelView(Tag, db.session))
    admin.add_view(CommentModelView(Comment, db.session))
