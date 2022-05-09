from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, session

from app.profile.forms import ChangePassForm
from ..models import Student, User
from .. import db
from flask_login import login_required, current_user
from . import profile
from ..email import send_email, send_congrat_email

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