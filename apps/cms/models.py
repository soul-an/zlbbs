# encoding: utf-8
# models.py by Anderson Huang at 2018/12/24 11:28
from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# cms权限二进制模型
class CMSPermission(object):
    # 0.所有权限，255的二进制表示 1111 1111
    ALL_PERMISSION = 0b11111111
    # 1.访问者权限
    VISITOR = 0b00000001
    # 2.管理帖子权限
    POSTER = 0b00000010
    # 3.管理评论权限
    COMMENTER = 0b00000100
    # 4.管理板块权限
    BOARDER = 0b00001000
    # 5.管理前台用户权限
    FRONTUSER = 0b00010000
    # 6.管理后台用户权限
    CMSUSER = 0b00100000
    # 7.管理后台管理员的权限
    ADMINER = 0b01000000


# 用户和角色多对多相关联的中间表
cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role_id', db.Integer, db.ForeignKey('cms_role.id'), primary_key=True),
    db.Column('cms_user_id', db.Integer, db.ForeignKey('cms_user.id'), primary_key=True)
)


# cms用户模型
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

    # 判断具有哪些权限
    @property
    def permissions(self):
        if not self.roles:
            return 0
        all_permissions = 0
        for role in self.roles:
            permissions = role.permissions
            all_permissions |= permissions
        return all_permissions

    # 判断是否具有某一权限
    def has_permission(self, permission):
        # all_permission = self.permissions
        # result = all_permission & permission == permission  # 做与运算
        # return result
        return self.permissions & permission == permission

    # 判断是否具有开发者权限
    @property
    def is_developer(self):
        return self.has_permission(CMSPermission.ALL_PERMISSION)


# 定义角色模型
class CMSRole(db.Model):
    __tablename = 'cms_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    permissions = db.Column(db.Integer, default=CMSPermission.VISITOR)

    # 关联用户和角色两个表
    users = db.relationship('CMSUser', secondary=cms_role_user, backref='roles')
