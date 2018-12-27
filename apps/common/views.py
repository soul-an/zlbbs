# encoding: utf-8
# views.py by Anderson Huang at 2018/12/24 11:28
from flask import Blueprint

bp = Blueprint('common', __name__, url_prefix='/common')


@bp.route('/')
def index():
    return 'common index'
