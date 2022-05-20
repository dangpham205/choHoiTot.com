from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from datetime import datetime


login_manager = LoginManager()
login_manager.login_view = 'auth.login_page'    #login_required sẽ direct đến trang này nếu chưa login
login_manager.login_message_category = 'info'       #tạo category cho flash


db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
moment = Moment()


def prettier_budget(budget):
    if len(str(budget)) >= 4:
        return '{:,}'.format(budget)
    else:
        return f"{budget}"

def length(list):
    return len(list)

def fromNow(string):
    timestamp = datetime.strptime(str(string), '%Y-%m-%d %H:%M:%S.%f')
    duration_in_second = (datetime.now() - timestamp).total_seconds()
    if 0 <= duration_in_second <= 44:
        return 'Vài giây trước'
    elif 45 <= duration_in_second <= 120:
        return 'Một phút trước'
    elif 121 <= duration_in_second <= 3600:          #90 tới 60 phút
        return f'{str(duration_in_second//60).split(".")[0]} phút trước'    
    elif 3601 <= duration_in_second <= 86400:       #1 giờ tới 24 giờ
        return f'{str(duration_in_second//(60*60)).split(".")[0]} giờ trước'
    elif 86401 <= duration_in_second <= 172800:       #24 giờ tới 48 giờ
        return f'Một ngày trước'
    elif 172801 <= duration_in_second <= 2592000:       #48 giờ tới 30 ngày
        return f'{str(duration_in_second//(24*60*60)).split(".")[0]} ngày trước'
    elif 2592001 <= duration_in_second <= 31104000:       #1 tháng tới 12 tháng
        return f'{str(duration_in_second//(30*24*60*60)).split(".")[0]} tháng trước'
    else:
        return 'Hơn 1 năm trước'
        
def fromNow2(string):
    timestamp = datetime.strptime(str(string), '%d/%m/%Y %H:%M:%S')
    duration_in_second = (datetime.now() - timestamp).total_seconds()
    if 0 <= duration_in_second <= 44:
        return 'Vài giây trước'
    elif 45 <= duration_in_second <= 120:
        return 'Một phút trước'
    elif 121 <= duration_in_second <= 3600:          #90 tới 60 phút
        return f'{str(duration_in_second//60).split(".")[0]} phút trước'    
    elif 3601 <= duration_in_second <= 86400:       #1 giờ tới 24 giờ
        return f'{str(duration_in_second//(60*60)).split(".")[0]} giờ trước'
    elif 86401 <= duration_in_second <= 172800:       #24 giờ tới 48 giờ
        return f'Một ngày trước'
    elif 172801 <= duration_in_second <= 2592000:       #48 giờ tới 30 ngày
        return f'{str(duration_in_second//(24*60*60)).split(".")[0]} ngày trước'
    elif 2592001 <= duration_in_second <= 31104000:       #1 tháng tới 12 tháng
        return f'{str(duration_in_second//(30*24*60*60)).split(".")[0]} tháng trước'
    else:
        return 'Hơn 1 năm trước'
    

def create_app():
    app = Flask(__name__, static_folder="../static")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///endterm.db'
    app.config['SECRET_KEY'] = '18a29538cdd94979294afa64'   #secret de co the hien thi form, python-->import os-->os.urandom(12).hex()
    app.config['RECAPTCHA_PUBLIC_KEY'] = "6LfOCtgfAAAAAOZlXMCa8tA4vXTmPPOoSY5FG1zV"
    app.config['RECAPTCHA_PRIVATE_KEY'] = "6LfOCtgfAAAAAKUxYIzTT_Jugz0kiHcYjGjm0TKB"
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    app.jinja_env.globals.update(prettier_budget=prettier_budget, length = length, fromNow = fromNow, fromNow2 = fromNow2)
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'ipos10d@gmail.com'
    app.config['MAIL_PASSWORD'] = 'ipos10diem'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail.init_app(app)

    
    # @app.shell_context_processor
    # def make_shell_context():
    #     return dict(db=db, User=User, Student=Student)

    @app.before_first_request
    def create_tables():
        db.create_all()


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .profile import profile as profile_blueprint
    app.register_blueprint(profile_blueprint, url_prefix='/profile')
    
    return app