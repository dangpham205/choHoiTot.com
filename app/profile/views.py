from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, session

from app.profile.forms import ChangePassForm, EditProfileForm, AddBudgetForm, Go2AddBudgetForm, Go2ManageBudgetForm
from ..models import Product, User, Budget
from .. import db
from hashlib import md5
from flask_login import login_required, current_user
from . import profile
from sqlalchemy import desc
from ..email import send_email, send_congrat_email

@profile.route('/<username>')
def profile_page(username):
    if username is not None:        
        user = User.query.filter_by(user_name = username).first_or_404()
        email= user.user_email
        email_hash = md5(email.encode("utf-8")).hexdigest()
        if user.user_score > 15000000:
            user_avatar = f"https://www.gravatar.com/avatar/{email_hash}?s=100&d=https://static.wikia.nocookie.net/leagueoflegends/images/2/29/Season_2019_-_Challenger_2.png/revision/latest/scale-to-width-down/250?cb=20181229234915"
        elif user.user_score > 5000000:
            user_avatar = f"https://www.gravatar.com/avatar/{email_hash}?s=100&d=https://static.wikia.nocookie.net/leagueoflegends/images/a/a3/Season_2019_-_Platinum_2.png/revision/latest/scale-to-width-down/250?cb=20181229234933"
        else:        
            user_avatar = f"https://www.gravatar.com/avatar/{email_hash}?s=100&d=https://static.wikia.nocookie.net/leagueoflegends/images/f/f4/Season_2019_-_Bronze_1.png/revision/latest/scale-to-width-down/250?cb=20181229234910"
        return render_template('profile/profile.html', user=user, user_avatar=user_avatar)

@profile.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    user = User.query.filter_by(user_name = current_user.user_name).first()
    if form.validate_on_submit():
        user.user_name = form.username.data
        user.user_fullname = form.fullname.data
        user.user_phone = form.phone.data
        user.bio = form.bio.data
        db.session.commit()
        flash('Trang cá nhân được cập nhật thành công !', category='success')
        return redirect(url_for('profile.profile_page', username=current_user.user_name))
    if form.errors != {}:       #if there are errors
        for error in form.errors.values():
            flash(f'{error}', category='danger')
    return render_template('profile/edit_profile.html', user=user, form=form)

@profile.route('manage_budget', methods=['GET', 'POST'])
@login_required
def manage_budget():
    form1 = Go2AddBudgetForm()
    form2 = Go2ManageBudgetForm()
    return render_template('profile/manage_budget.html', form1=form1, form2=form2)

@profile.route('budget_history', methods=['GET', 'POST'])
@login_required
def budget_history():
    records = Budget.query.filter_by(user_id=current_user.id).order_by(desc(Budget.id))
    return render_template('profile/budget_history.html', records = records)


@profile.route('/add_budget', methods=['GET', 'POST'])
@login_required
def add_budget():
    form = AddBudgetForm()
    user = User.query.filter_by(user_name = current_user.user_name).first()
    if form.validate_on_submit():
        if (form.amount.data.isnumeric() == False):
            flash('Giá tiền có kiểu dữ liệu là số !', category='danger')
        else:
            token = user.generate_confirmation_token()          
            send_email(user.user_email, 'mail/add_budget', user=user, token=token, amount=form.amount.data)
            flash('Hãy xác nhận giao dịch thông qua Email của bạn !', category='success')
            return redirect(url_for('profile.manage_budget'))
    return render_template('profile/add_budget.html', user=user, form=form)
    
@profile.route('/confirm_add_budget/<amount>/<token>')
@login_required
def confirm_add_budget(amount,token):
    if current_user.confirm(token) == 'TRUE':
        current_user.user_budget += int(amount)
        db.session.commit()
        record_amount = prettier_budget(int(amount))
        record_budget = prettier_budget(current_user.user_budget)
        budget_record = Budget(description='Tiền chuyển vào',
                                amount='+'+ record_amount,
                                budget=record_budget,
                                user_id= current_user.id)
        db.session.add(budget_record)
        db.session.commit()
        flash('Bạn đã nạp tiền vào tài khoản thành công!.', category='success')
    elif current_user.confirm(token) == 'TOUCHED':
        flash('Link nạp tiền không hợp lệ. ', category='danger')
    elif current_user.confirm(token) == 'EXPIRED':
        flash('Link nạp tiền đã hết hạn. ', category='danger')
    else:
        flash('Ôi không ...', category='danger')
    return redirect(url_for('main.home_page'))



@profile.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password() :
    form = ChangePassForm()
    if form.validate_on_submit():
        user = current_user
        if user is not None and user.check_password(form.old_password.data):
            user.password = form.new_password.data
            db.session.commit()
            flash('Mật khẩu được đổi thành công.', category='success')
            return redirect(url_for('main.home_page'))
        flash('Sai mật khẩu !.', category='info')
    return render_template('profile/change_password.html', form=form)

def prettier_budget(budget):
        if len(str(budget)) >= 4:
            return '{:,}'.format(budget)
        else:
            return f"{budget}"