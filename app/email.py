from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message("TDTU iBanking",
                  sender='Flasky Admin <flasky@example.com>', recipients=[to])
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

def send_congrat_email(to, subject, **kwargs):
    app = current_app._get_current_object()
    msg = Message("TDTU iBanking",
                  sender='Flasky Admin <flasky@example.com>', recipients=[to])
    msg.body = subject
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
