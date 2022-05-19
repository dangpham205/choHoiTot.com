from flask import render_template, redirect, session, url_for, flash

from app.email import send_email
from ..models import User
from .forms import ForgotPassForm, RegisterForm, LoginForm, SendForgotPassForm
from .. import db
from flask_login import current_user, login_user, logout_user
from . import auth


@auth.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(user_name=form.username.data,
                        user_fullname=form.fullname.data,
                        user_phone=form.phone.data,
                        user_email=form.email.data,
                        password=form.password1.data)   
                        #không truyền password_hash mà truyền password, để hàm setter trong model generate tự hash password_hash
        db.session.add(new_user)
        db.session.commit()
        token = new_user.generate_confirmation_token()          
        send_email(new_user.user_email, 'mail/confirm_register', user=new_user, token=token)
        session['unconfirmed_user'] = form.email.data
        flash('Một Email đã được gửi cho bạn, hãy kiểm tra và xác thực tài khoản !', category='success')
        return redirect(url_for('auth.login_page'))
    if form.errors != {}:       #if there are errors
        for error in form.errors.values():
            flash(f'{error}', category='danger')
    return render_template('auth/register.html', form=form)

@auth.route('/confirm_register/<token>')
def confirm_register(token):
    if 'unconfirmed_user' in session:
        email = session['unconfirmed_user']
        user = User.query.filter_by(user_email=email).first()     
        session.pop('unconfirmed_user')
        if user.confirmed:
            return redirect(url_for('main.home_page'))
        if user.confirm(token, change_confirmed = True) == "TRUE":
            login_user(user)
            flash('Bạn đã xác thực tài khoản thành công, Xin Chào !', category='success')
        else:
            flash('Email xác thực đã hết thời hạn.', category='danger')
    return redirect(url_for('main.home_page'))

@auth.route('/forgot_pass_request', methods=['GET', 'POST'])
def forgot_pass_request():
    form = SendForgotPassForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data.lower()).first()
        if user is not None :
            token = user.generate_confirmation_token()          
            send_email(user.user_email, 'mail/forgot_password', user=user, token=token)
            flash('Bạn đã nhận được một Email để xác nhận thay đổi mật khẩu.'
                ' Hãy kiểm tra ! ', category='success')
            return redirect(url_for('auth.login_page'))
    return render_template('auth/forgot_pass_request.html', form=form)

@auth.route('/forgot_pass/<token>', methods=['GET', 'POST'])
def forgot_pass(token):
    form = ForgotPassForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated and token is not None:
            flag = User.reset_password(token=token, new_password=form.new_password.data)
            if flag:
                flash('Mật khẩu được đổi thành công.', category='success')
                return redirect(url_for('auth.login_page'))
            else:
                flash('Email xác nhận mật khẩu mới đã hết thời hạn.', category='danger')
                return render_template('auth/forgot_pass.html', form=form)
    return render_template('auth/forgot_pass.html', form=form)

@auth.route('/unconfirmed')
def unconfirmed():
    return render_template('auth/unconfirmed.html')

@auth.route('/resend-confirmation-email')
def resend_confirmation():
    if 'unconfirmed_user' in session:
        email = session['unconfirmed_user']
        user = User.query.filter_by(user_email=email).first()    
        if not user.confirmed:
            new_token = user.generate_confirmation_token() 
            send_email(user.user_email, 'mail/confirm_register', user=user, token=new_token)
            flash('Một email xác thực mới đã được gửi vào hòm thư của bạn. ', category='success')
    return redirect(url_for('main.home_page'))

@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(user_email=form.email.data).first()
        if attempted_user:
            if attempted_user.confirmed == False:
                session['unconfirmed_user'] = form.email.data
                return redirect(url_for('auth.unconfirmed'))
        if attempted_user and attempted_user.check_password(form.password.data):
            login_user(attempted_user)
            flash('Đăng nhập thành công !', category='success')
            return redirect(url_for('main.chotot_page', category='all'))
        else:
            flash('Lỗi đăng nhập !', category='danger')      

    return render_template('auth/login.html', form=form)

@auth.route('/logout')
def logout_page():
    logout_user()
    flash('Đăng xuất thành công !', category='info')
    return redirect(url_for('main.home_page'))