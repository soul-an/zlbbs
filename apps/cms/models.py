# encoding: utf-8
# models.py by Anderson Huang at 2018/12/24 11:28
from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class CMSUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    # 对外字段名叫做password
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

    # 重写初始化函数
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    # 对内的字段名叫做_password
    @property
    def password(self):
        return self._password

    # 加密密码
    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    # 验证密码
    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result
