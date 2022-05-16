from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment

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

def create_app():
    app = Flask(__name__, static_folder="../static")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///endterm.db'
    app.config['SECRET_KEY'] = '18a29538cdd94979294afa64'   #secret de co the hien thi form, python-->import os-->os.urandom(12).hex()
    app.config['RECAPTCHA_PUBLIC_KEY'] = "6LfOCtgfAAAAAOZlXMCa8tA4vXTmPPOoSY5FG1zV"
    app.config['RECAPTCHA_PRIVATE_KEY'] = "6LfOCtgfAAAAAKUxYIzTT_Jugz0kiHcYjGjm0TKB"
    app.config['UPLOAD_FOLDER'] = 'images/avatar'
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)
    app.jinja_env.globals.update(prettier_budget=prettier_budget)
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