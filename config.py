
# import os

# class Config:
#     SECRET_KEY = 'your_secret_key'
#     SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Aq112211@localhost/postgres'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     UPLOADED_PHOTOS_DEST = os.path.join(os.path.dirname(__file__), 'static', 'images')  # 静态文件目录
#     UPLOADS_DEFAULT_DEST = os.path.join(os.path.dirname(__file__), 'static', 'images')  # 同样的目录
#     UPLOADS_DEFAULT_URL = '/static/images/'  # URL 访问路径
import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False') == 'True'
    UPLOADED_PHOTOS_DEST = os.getenv('UPLOADED_PHOTOS_DEST', os.path.join(os.path.dirname(__file__), 'static', 'images'))
    UPLOADS_DEFAULT_DEST = os.getenv('UPLOADS_DEFAULT_DEST', os.path.join(os.path.dirname(__file__), 'static', 'images'))
    UPLOADS_DEFAULT_URL = os.getenv('UPLOADS_DEFAULT_URL', '/static/images/')
