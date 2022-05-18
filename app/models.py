from . import db, bcrypt, login_manager
from flask_login import UserMixin
from datetime import datetime
import json
from datetime import datetime
from flask import current_app, flash
import authlib.jose.errors
from authlib.jose import JsonWebSignature

#import class UserMixin để class User kế thừa
#nếu kế thừa thì trong User đỡ phải implement các method mà flask_login đòi
#kh kế thừa thì phải có cái method trong link:  https://flask-login.readthedocs.io/en/latest/#how-it-works

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)        #phải để id vì đang có lỗi import, mà hàm get_id của flask_login đòi column tên là id
    user_name = db.Column(db.String(20), nullable=False)
    user_fullname = db.Column(db.String(20), nullable=False)
    user_phone = db.Column(db.String(12), nullable=False)
    user_email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(60), nullable=False)            #phải để 60 vì hash ra sẽ gất dài
    user_budget = db.Column(db.Integer(), nullable=False, default=20000000000)
    avatar = db.Column(db.String(40), nullable=False, default="default.jpg")
    confirmed = db.Column(db.Boolean, default=False)
    bio = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default = datetime.utcnow())
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow())
    user_score = db.Column(db.Integer(), nullable=False, default=0)     #dựa vào cột này để set verify mark cho ng dùng
    user_paid_list = db.relationship('Product', backref = 'owned_user', lazy=True)

    def update_last_seen(self):
        self.last_seen = datetime.utcnow()
        # db.session.add(self)
        db.session.commit()

    #tạo ra 1 property tên password 
    @property
    def password(self):
        return self.password

    #và password sẽ là input được hash sau đó gắn vô user_password
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    @property
    def prettier_budget(self):
        if len(str(self.user_budget)) >= 4:
            return '{:,}'.format(self.user_budget) + ' đồng'
        else:
            return f"{self.user_budget}" + " đồng"

    def can_purchase(self, product):
        return self.user_budget >= product.price

    def generate_confirmation_token(self):
        jws = JsonWebSignature()
        protected = {'alg': 'HS384'}  
        payload = '{"confirm":' + str(self.id) + ',"timestamp":"' + str(datetime.now()) + '"}'
        secret = current_app.config['SECRET_KEY']
        token = jws.serialize_compact(protected, payload, secret)
        return token
    
    def confirm(self, token, expiration=180, change_confirmed=False):
    # Deserialize a JWS Compact Serialization
        jws = JsonWebSignature()
        try:
            data = jws.deserialize_compact(token, key=current_app.config['SECRET_KEY'])
        except authlib.jose.errors.BadSignatureError:       #KHI TOKEN BỊ TOUCH(CHỈNH SỬA)
            return 'TOUCHED'
        except:
            return 'OTHERS'
        # Validate timestamp and token
        decoded_payload = json.loads(data.get('payload'))
        timestamp = datetime.strptime(decoded_payload.get('timestamp'), '%Y-%m-%d %H:%M:%S.%f')
        duration_in_second = (datetime.now() - timestamp).total_seconds()
        user_id = decoded_payload.get('confirm')
        if duration_in_second < 0 or duration_in_second > expiration or user_id != self.id:
            return 'EXPIRED'
        else:
            if change_confirmed == True:
                self.confirmed = True
                # db.session.add(self)
                db.session.commit()

            return 'TRUE'
    
    def reset_password(token, new_password, expiration=180):
    # Deserialize a JWS Compact Serialization
        jws = JsonWebSignature()
        try:
            data = jws.deserialize_compact(token, key=current_app.config['SECRET_KEY'])
        except authlib.jose.errors.BadSignatureError:       #KHI TOKEN BỊ TOUCH(CHỈNH SỬA)
            return False
        except:
            return False
        # Validate timestamp and token
        decoded_payload = json.loads(data.get('payload'))
        timestamp = datetime.strptime(decoded_payload.get('timestamp'), '%Y-%m-%d %H:%M:%S.%f')
        duration_in_second = (datetime.now() - timestamp).total_seconds()
        user_id = decoded_payload.get('confirm')
        user = User.query.filter_by(id=user_id).first()
        if duration_in_second < 0 or duration_in_second > expiration :
            return False
        else:
            user.password = new_password
            # db.session.add(user)
            db.session.commit()
            return True

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.Text())
    date = db.Column(db.String(40), nullable=False, default=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    category = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(40))
    status = db.Column(db.String(40), nullable=False, default="SELLING")
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id')) 

    def purchase(self, user):
        if(self.status=='SELLING'):
            old_owner = User.query.filter_by(id=self.owner_id).first()
            old_owner.user_score += self.price
            old_owner.user_budget += self.price
            self.owner_id = user.id
            self.status = 'OWNED'
            self.date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            user.user_budget -= self.price
            db.session.commit()
            record_amount = prettier_budget(int(self.price))
            record_budget = prettier_budget(user.user_budget)
            record_budget_2 = prettier_budget(old_owner.user_budget)
            budget_record_mua = Budget(description='Tiền chuyển ra',
                                amount='-'+ record_amount,
                                budget=record_budget,
                                user_id= user.id)
            budget_record_ban = Budget(description='Tiền chuyển vào',
                                amount='+'+ record_amount,
                                budget=record_budget_2,
                                user_id= user.id)
            db.session.add(budget_record_mua)
            db.session.add(budget_record_ban)
            db.session.commit()
            flash(f"Chúc mừng! Bạn vừa mua {self.name} với giá {self.price} đồng!", category='success')
            return True
        else:
            flash(f'Sản phẩm đã được mua bởi người dùng khác.' , category='danger')
            return False

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text())          #tiền chuyển ra, vào
    date = db.Column(db.String(40), nullable=False, default=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    amount = db.Column(db.Text())        # +5500, -600
    budget = db.Column(db.Text())        # số dư
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Text())          
    date = db.Column(db.String(40), nullable=False, default=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    product_name = db.Column(db.Text())  
    total = db.Column(db.Text())         
    other_id = db.Column(db.Integer) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 

class Favourite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 

def prettier_budget(budget):
        if len(str(budget)) >= 4:
            return '{:,}'.format(budget)
        else:
            return f"{budget}"

