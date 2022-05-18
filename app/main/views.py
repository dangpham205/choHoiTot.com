from datetime import datetime
import os
from unicodedata import name
from flask import render_template, redirect, url_for, flash, request, session

from ..models import Product, User
from .forms import AddForm, SearchForm, UpdateForm
from .. import db
from flask_login import login_required, current_user
from . import main
from ..email import send_email, send_congrat_email
from werkzeug.utils import secure_filename



@main.route('/')
@main.route('/home')
def home_page():
    return render_template("home.html")

@main.route('/chotot/<category>', methods=['GET', 'POST'])
@login_required             #yêu cầu user phải đăng nhập mới được vô trang market ==> file init phải có thêm dòng 13,14
def chotot_page(category):
    addForm = AddForm()
    searchForm = SearchForm()
    stuId = ""
    if request.method == 'POST':
        # student_to_search = Student.query.filter_by(student_id=(searchForm.keyword.data).strip(),student_owner=None).first()
        # if student_to_search:
        #     stuId = (searchForm.keyword.data).strip()
        # else:
        #     flash(f"Student Not Found !!", category='danger')
        
        # students = Student.query.filter_by(student_owner=None, student_id=stuId)    #return all the items in the db MÀ CHƯA CÓ OWNER
        # owned_students = Student.query.filter_by(student_owner=current_user.id) 
        return render_template('market/chotot.html', 
                                # students=students, 
                                # owned_students = owned_students, 
                                addForm= addForm, 
                                searchForm=searchForm)

    if request.method == 'GET':
        if category == "all" or category == 'Tất cả':
            category = 'Tất cả'
            products = Product.query.filter(Product.status =='SELLING', 
                                        Product.owner_id != current_user.id
                                        ).order_by(Product.id.desc()).all() 
        else:    
            products = Product.query.filter(Product.status =='SELLING', 
                                        Product.owner_id != current_user.id,
                                        Product.category == category).order_by(Product.id.desc()).all()    #return all the items in the db MÀ CHƯA CÓ OWNER
        # owned_students = Student.query.filter_by(student_owner=current_user.id) 
        return render_template('market/chotot.html', 
                                products = products, 
                                category = category,
                                # owned_students = owned_students, 
                                addForm= addForm, 
                                searchForm=searchForm)

@main.route('/product_detail/<product_id>', methods=['GET', 'POST'])
def detail_page(product_id):
    # if product_id:
    product = Product.query.filter_by(id=product_id).first()
    owner = User.query.filter_by(id=product.owner_id).first()
    others = Product.query.filter(Product.category == product.category,
                                Product.owner_id != current_user.id,
                                Product.id != product.id).limit(5).all()
    return render_template('market/product_detail.html', 
                            product = product , 
                            owner = owner, 
                            others = others,
                            )
    

@main.route('/purchase/<product_id>', methods=['POST','GET'])
@login_required
def purchase(product_id):
    # Purchase function
    if request.method == 'POST':
        product = Product.query.filter_by(id = product_id, status= 'SELLING').first()
        if product:
            print(product.name)
            if current_user.can_purchase(product):
                user = current_user
                token = user.generate_confirmation_token()      
                send_email(user.user_email, 'mail/confirm_purchase', user=user, token=token, product=product)
                flash("Email xác thực cho giao dịch này đã được gửi đến hộp thư của bạn! ", category='success')    
            else:
                flash(f"Số dư trong tài khoản của bản không đủ để mua {product.name}!", category='danger')
        else:
            flash('Sản phẩm này không phải để bán!', category='danger')
    return redirect(url_for('main.detail_page', product_id=product_id))

@main.route('/confirm_email/<product_id>/<token>')
@login_required
def confirm_purchase(product_id,token):
    if current_user.confirm(token) == 'TRUE':
        product = Product.query.filter_by(id = product_id).first()
        old_owner = User.query.filter_by(id=product.owner_id).first()
        if product.purchase(current_user) == True:
            print(product.owner_id)
            print(product.status)
            send_email(current_user.user_email, 'mail/purchase_success_buyer', user=current_user, product=product, owner = old_owner)
            # send_email(old_owner.user_email, 'mail/purchase_success', user=current_user, product=product, owner = old_owner)
    elif current_user.confirm(token) == 'TOUCHED':
        flash('Link xác nhận mua hàng không hợp lệ. ', category='danger')
    elif current_user.confirm(token) == 'EXPIRED':
        flash('Link xác nhận mua hàng đã hết thời hạn. ', category='danger')
    else:
        flash('Đã xảy ra lỗi khi xác thực giao dịch.', category='danger')
    return redirect(url_for('main.chotot_page', category='all'))

@main.route('/product_owned', methods=['POST','GET'])
@login_required
def product_owned():
    form = UpdateForm()
    user = User.query.filter_by(id = current_user.id).first_or_404()
    products = Product.query.filter(Product.status =='OWNED', 
                                    Product.owner_id == user.id
                                    ).order_by(Product.id.desc()).all() 
    number_of_products = len(products)
    return render_template('market/product_owned.html', 
                            user=user, 
                            products = products, 
                            form = form,
                            number_of_products = number_of_products)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    addForm = AddForm()
    if request.method == 'POST':
        file =addForm.file.data#First grab the file
        if (addForm.price.data.isnumeric() == False):
            flash('Hãy nhập giá tiền hợp lệ !!', category='danger')
        elif allowed_file(file.filename) == False:
            flash(f'File ảnh không hợp lệ!', category='danger')
        else:
            add_product = Product(description=addForm.description.data,
                            name=addForm.name.data,
                            price=addForm.price.data,
                            category=addForm.category.data,
                            owner_id=current_user.id)
            db.session.add(add_product)
            db.session.commit()
            file.filename = f"{add_product.id}."+ file.filename.rsplit('.', 1)[1].lower()
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../static/product', secure_filename(file.filename)))#Then save the file
            add_product.image = f"{add_product.id}."+ file.filename.rsplit('.', 1)[1].lower()
            db.session.commit()
            flash(f'Sản phẩm {addForm.name.data} đã được đăng bán thành công !!' , category='success')
    return redirect(url_for('main.chotot_page', category='all'))

@main.route('/update/<product_id>', methods=['GET', 'POST'])
@login_required
def update(product_id):
    form = UpdateForm()
    haveChange = False
    product = Product.query.filter_by(id = product_id).first()
    if request.method == 'POST':
        if form.name.data :
            product.name = form.name.data
            haveChange = True
        if form.price.data :
            if (form.price.data.isnumeric() == False):
                flash('Hãy nhập giá tiền hợp lệ !!', category='danger')
                return redirect(url_for('profile.profile_page', username=current_user.user_name))
            else:
                product.price = form.price.data
                haveChange = True
        if form.description.data :
            product.description = form.description.data
            haveChange = True
        if form.file.data:
            file = form.file.data
            if allowed_file(file.filename) == False:
                flash(f'File ảnh không hợp lệ!', category='danger')
            else:
                file.filename = f"{product.id}."+ file.filename.rsplit('.', 1)[1].lower()
                file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../static/product', secure_filename(file.filename)))#Then save the file
                product.image = f"{product.id}."+ file.filename.rsplit('.', 1)[1].lower()
                haveChange = True
        if form.category.data != '...':
            product.category = form.category.data
            haveChange = True
        if haveChange == True:
            db.session.commit()
            flash('Thông tin sản phẩm đã được cập nhật thành công !', category='success')
        elif haveChange == False:
            flash('Hãy điền các trường thông tin mà bạn muốn cập nhật!', category='info')
    return redirect(url_for('profile.profile_page', username=current_user.user_name))

@main.route('/resell/<product_id>', methods=['GET', 'POST'])
@login_required
def resell(product_id):
    form = UpdateForm()
    product = Product.query.filter_by(id = product_id).first()
    if request.method == 'POST':
        if form.name.data :
            product.name = form.name.data
        if form.price.data :
            if (form.price.data.isnumeric() == False):
                flash('Hãy nhập giá tiền hợp lệ !!', category='danger')
                return redirect(url_for('main.product_owned'))
            else:
                product.price = form.price.data
        if form.description.data :
            product.description = form.description.data
        if form.file.data:
            file = form.file.data
            if allowed_file(file.filename) == False:
                flash(f'File ảnh không hợp lệ!', category='danger')
            else:
                file.filename = f"{product.id}."+ file.filename.rsplit('.', 1)[1].lower()
                file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../static/product', secure_filename(file.filename)))#Then save the file
                product.image = f"{product.id}."+ file.filename.rsplit('.', 1)[1].lower()
        if form.category.data != '...':
            product.category = form.category.data
        product.date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        product.status = 'SELLING'
        db.session.commit()
        flash('Sản phẩm đã được đăng bán thành công !', category='success')

    return redirect(url_for('main.product_owned'))


@main.route('/delete/<product_id>', methods=['POST','GET'])
@login_required
def delete(product_id):
    product = Product.query.filter_by(id = product_id).first()
    if request.method == 'POST':
        if product:
            db.session.delete(product)
            db.session.commit()
            flash('Sản phẩm đã xóa thành công!', category='success')
        else:
            flash('Không thể xóa sản phẩm!', category='danger')
    return redirect(url_for('profile.profile_page', username=current_user.user_name))
    

def prettier_budget(budget):
        if len(str(budget)) >= 4:
            return '{:,}'.format(budget)
        else:
            return f"{budget}"