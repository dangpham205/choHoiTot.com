from datetime import datetime
import os
import random
from flask import render_template, redirect, request, url_for, flash
from app.main.forms import UpdateForm
from app.profile.forms import ChangePassForm, ConfirmAddBudgetForm, EditProfileForm, AddBudgetForm, Go2AddBudgetForm, Go2ManageBudgetForm, UploadFileForm
from ..models import Otp, Product, User, Budget
from .. import db
from flask_login import login_required, current_user
from . import profile
from sqlalchemy import desc
from ..email import send_email
from werkzeug.utils import secure_filename

import app



@profile.route('/<id>', methods=['GET', 'POST'])
def profile_page(id):
    updateForm = UpdateForm()
    if id is not None:        
        if current_user.is_authenticated:
            current_user.update_last_seen()
        user = User.query.filter_by(id = id).first_or_404()
        select = request.form.get('sort')
        if select == 'date':
            products = Product.query.filter(Product.status =='SELLING', 
                                            Product.owner_id == user.id
                                            ).order_by(Product.date.desc()).all() 
        elif select == 'price_az':
            products = Product.query.filter(Product.status =='SELLING', 
                                            Product.owner_id == user.id
                                            ).order_by(Product.price).all() 
        elif select == 'price_za':
            products = Product.query.filter(Product.status =='SELLING', 
                                            Product.owner_id == user.id
                                            ).order_by(Product.price.desc()).all() 
        elif select == 'name_az':
            products = Product.query.filter(Product.status =='SELLING', 
                                            Product.owner_id == user.id
                                            ).order_by(Product.name).all() 
        elif select == 'name_za':
            products = Product.query.filter(Product.status =='SELLING', 
                                            Product.owner_id == user.id
                                            ).order_by(Product.name.desc()).all() 
        else:
            products = Product.query.filter(Product.status =='SELLING', 
                                            Product.owner_id == user.id
                                            ).order_by(Product.date.desc()).all()
        number_of_products = len(products)
        return render_template('profile/profile.html', user=user, products = products, form = updateForm, number_of_products = number_of_products)

@profile.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    user = User.query.filter_by(user_name = current_user.user_name).first()
    haveChange = False
    current_user.update_last_seen()
    if form.validate_on_submit():
        if form.username.data :
            user_to_check = User.query.filter_by(user_name=form.username.data).first()
            if user_to_check and user_to_check.id == user.id:
                flash('Hãy nhập 1 username khác', category='danger')
                return render_template('profile/edit_profile.html', user=user, form=form)
            else:
                user.user_name = form.username.data
                haveChange = True
        if form.fullname.data:
            user.user_fullname = form.fullname.data
            haveChange = True
        if form.phone.data:
            if form.phone.data.isnumeric() == False or len(form.phone.data) > 12 or len(form.phone.data) <8:
                flash('Hãy nhập 1 số điện thoại hợp lệ', category='danger')
                return render_template('profile/edit_profile.html', user=user, form=form)
            else:
                user.user_phone = form.phone.data
                haveChange = True
        if form.bio.data:
            user.bio = form.bio.data
            haveChange = True
        if haveChange == True:
            db.session.commit()
            flash('Trang cá nhân được cập nhật thành công !', category='success')
            return redirect(url_for('profile.profile_page', id=current_user.id))
        elif haveChange == False:
            flash('Hãy điền các trường thông tin mà bạn muốn cập nhật!', category='info')
    return render_template('profile/edit_profile.html', user=user, form=form)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@profile.route('change_avatar', methods=['GET', 'POST'])
@login_required
def change_avatar():
    current_user.update_last_seen()
    form = UploadFileForm()
    if form.validate_on_submit():
        file =form.file.data#First grab the file
        if allowed_file(file.filename):
            file.filename = f"{current_user.id}."+ file.filename.rsplit('.', 1)[1].lower()
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../static/avatar', secure_filename(file.filename)))#Then save the file
            current_user.avatar = f"{current_user.id}."+ file.filename.rsplit('.', 1)[1].lower()
            db.session.commit()
            flash(f'Ảnh đại diện đã được cập nhật!', category='info')
            return render_template('profile/change_avatar.html', form = form)
        else:
            flash(f'File ảnh không hợp lệ!', category='danger')
    return render_template('profile/change_avatar.html', form = form)

@profile.route('manage_budget', methods=['GET', 'POST'])
@login_required
def manage_budget():
    form1 = Go2AddBudgetForm()
    form2 = Go2ManageBudgetForm()
    return render_template('profile/manage_budget.html', form1=form1, form2=form2)

@profile.route('budget_history', methods=['GET', 'POST'])
@login_required
def budget_history():
    current_user.update_last_seen()
    records = Budget.query.filter_by(user_id=current_user.id).order_by(desc(Budget.id))
    return render_template('profile/budget_history.html', records = records)


@profile.route('/add_budget', methods=['GET', 'POST'])
@login_required
def add_budget():
    form = AddBudgetForm()
    user = User.query.filter_by(id = current_user.id).first()
    if user.last_add_budget:        #NẾU CÓ TỒN TẠI last_add_budget
        timestamp = datetime.strptime(user.last_add_budget, '%d/%m/%Y %H:%M:%S')
        duration_in_second = (datetime.now() - timestamp).total_seconds()
        if (duration_in_second > 180):      # nếu lần cuối request nạp đã quá 3 phút
            user.status = True
            otps = Otp.query.filter(Otp.status =='PENDING',  
                        Otp.user_id == user.id,).all()
            for otp in otps:
                otp.status = "EXIPRED"          #lần cuối request nạp đã quá 3 phút ==> sẽ không còn otp nào còn hạn
            db.session.commit()
    if form.validate_on_submit():
        if (form.amount.data.isnumeric() == False):
            flash('Giá tiền có kiểu dữ liệu là số !', category='danger')
        else:
            if user.status == False:
                flash("Hiện đang có 1 giao dịch nạp tiền khác đang được thực hiện!", category='info')
                return redirect(url_for('profile.confirm_add_budget'))
            elif user.status == True:
                user.status = False
                user.last_add_budget = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                otp = Otp(amount= int(form.amount.data), 
                            user_id = current_user.id,
                            code = '{:06}'.format(random.randrange(1, 1000000)),
                            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S") 
                            )
                db.session.add(otp)
                db.session.commit()
                send_email(user.user_email, 'mail/add_budget', user=user, otp = otp )
                flash('Hãy nhập mã OTP vừa được gửi đến email của bạn !', category='success')
                return redirect(url_for('profile.confirm_add_budget'))
    return render_template('profile/add_budget.html', user=user, form=form)
    
@profile.route('/confirm_add_budget', methods=['GET', 'POST'])
@login_required
def confirm_add_budget():
    form = ConfirmAddBudgetForm()
    user = current_user
    if form.validate_on_submit():
        otp = Otp.query.filter(Otp.status =='PENDING', 
                                Otp.user_id == user.id,
                                Otp.code == form.otp.data
                                ).order_by(Otp.id.desc()).first()
        if otp:
            timestamp = datetime.strptime(otp.timestamp, '%d/%m/%Y %H:%M:%S')
            duration_in_second = (datetime.now() - timestamp).total_seconds()
            if duration_in_second > 180:
                otp.status = 'EXPIRED'
                user.status = True
                db.session.commit()
                flash("Mã OTP đã hết hạn, hãy gửi yêu cầu nạp tiền khác!", category='info')
                return redirect(url_for('profile.add_budget'))
            elif duration_in_second <= 180:
                otp.status = 'SUCCEED'
                current_user.user_budget += otp.amount
                current_user.status = True
                db.session.commit()
                record_amount = prettier_budget(otp.amount)
                record_budget = prettier_budget(current_user.user_budget)
                budget_record = Budget(description='Tiền chuyển vào',
                                        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                                        amount='+'+ record_amount,
                                        budget=record_budget,
                                        user_id= current_user.id)
                db.session.add(budget_record)
                db.session.commit()
                send_email(user.user_email, 'mail/add_budget_success', user=user, budget = budget_record )
                flash('Bạn đã nạp tiền vào tài khoản thành công!', category='success')
                return redirect(url_for('profile.budget_history'))
        else:        
            flash("Mã OTP không hợp lệ!", category='danger')
    return render_template('profile/confirm_add_budget.html', user=user, form=form)

@profile.route('/resend_add_budget', methods=['GET', 'POST'])
@login_required
def resend_add_budget() :
    user = current_user
    otp = Otp.query.filter(Otp.status =='PENDING', 
                            Otp.user_id == user.id,
                            ).order_by(Otp.id.desc()).first()
    if otp:
        otp.timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        otp.code = '{:06}'.format(random.randrange(1, 1000000))
        user.last_add_budget = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        db.session.commit()
        send_email(user.user_email, 'mail/add_budget', user=user, otp = otp )
        flash('Hãy nhập mã OTP vừa được gửi đến email của bạn !', category='success')
    else:           #ở trong màn OTP quá 3 phút
        flash('Hãy thực hiện giao dịch khác !', category='success')
        return redirect(url_for('profile.add_budget'))
    return redirect(url_for('profile.confirm_add_budget'))


@profile.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password() :
    current_user.update_last_seen()
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