# encoding: utf-8
# exts.py by Anderson Huang at 2018/12/24 11:18
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

"""
防止循环利用的exts
"""

db = SQLAlchemy()
mail = Mail()
