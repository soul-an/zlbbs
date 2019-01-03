# encoding: utf-8
# exts.py by Anderson Huang at 2018/12/24 11:18
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from utils.alidayu import AlidayuAPI

"""
防止循环利用的exts
"""

db = SQLAlchemy()  # sqlalchemy数据库对象
mail = Mail()   # mail对象
alidayu = AlidayuAPI()   # 阿里大于api对象
