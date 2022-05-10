from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, session

from app.profile.forms import ChangePassForm, EditProfileForm
from ..models import Student, User
from .. import db
from hashlib import md5
from flask_login import login_required, current_user
from . import profile
from ..email import send_email, send_congrat_email

@profile.route('/<username>')
def profile_page(username):
    if username is not None:        
        user = User.query.filter_by(user_name = username).first_or_404()
        email= user.user_email
        email_hash = md5(email.encode("utf-8")).hexdigest()
        user_avatar = f"https://www.gravatar.com/avatar/{email_hash}?s=100&d=https://lolslaves.com/wp-content/uploads/2020/01/3.png"
        # role_id = str(current_user.role)
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
        flash('Update profile succeed !', category='success')
        return redirect(url_for('profile.profile_page', username=current_user.user_name))
    if form.errors != {}:       #if there are errors
        for error in form.errors.values():
            flash(f'{error}', category='danger')
    return render_template('profile/edit_profile.html', user=user, form=form)


@profile.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password() :
    form = ChangePassForm()
    if form.validate_on_submit():
        user = current_user
        if user is not None and user.check_password(form.old_password.data):
            user.password = form.new_password.data
            db.session.commit()
            flash('Password changed succeed.', category='success')
            return redirect(url_for('main.home_page'))
        flash('Wrong password!.', category='info')
    return render_template('profile/change_password.html', form=form)