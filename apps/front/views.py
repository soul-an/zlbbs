# encoding: utf-8
# views.py by Anderson Huang at 2018/12/24 11:28
from flask import Blueprint

bp = Blueprint('front', __name__)


@bp.route('/')
def index():
    return 'front index'
