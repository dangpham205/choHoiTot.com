from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail



login_manager = LoginManager()
login_manager.login_view = 'auth.login_page'    #login_required sẽ direct đến trang này nếu chưa login
login_manager.login_message_category = 'info'       #tạo category cho flash


db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()

def create_app():
    app = Flask(__name__, static_folder="../static")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///endterm.db'
    app.config['SECRET_KEY'] = '18a29538cdd94979294afa64'   #secret de co the hien thi form, python-->import os-->os.urandom(12).hex()
    # login_manager = LoginManager(app)
    # login_manager.login_view = 'login_page'         #tên của method trong view để dẫn đến trang login
    # login_manager.login_message_category = 'info'       #tạo category cho flash
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'ipos10d@gmail.com'
    app.config['MAIL_PASSWORD'] = 'ipos10diem'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail.init_app(app)


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app