from datetime import datetime
from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors

@main.app_context_processor
def inject_now():
    return {'now': datetime.utcnow()}