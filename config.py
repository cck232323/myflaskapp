import os

class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Aq112211@localhost/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADED_PHOTOS_DEST = os.path.join('static', 'images')  # 静态文件目录
