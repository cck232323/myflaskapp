from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads, ALL
from flask_login import LoginManager
from config import Config
from flask_migrate import Migrate
db = SQLAlchemy()
login_manager = LoginManager()
CUSTOM_IMAGES = IMAGES + ('jfif',)

photos = UploadSet('photos', CUSTOM_IMAGES)
migrate = Migrate()  # 初始化 migrate

 
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    configure_uploads(app, photos)  # 配置 photos
    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .admin import init_admin  # 导入和调用 init_admin
    init_admin(app)
    return app


