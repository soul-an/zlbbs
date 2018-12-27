# encoding: utf-8
# forms.py by Anderson Huang at 2018/12/24 11:29
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Email, InputRequired, Length, EqualTo
from apps.forms import BaseForm  # 导入和继承基础表单验证类
from utils import zlcache
from wtforms import ValidationError
from flask import g

"""
表单验证
"""


# 登陆表单验证
class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确格式的邮箱！'), InputRequired(message='请输入邮箱地址')])
    password = StringField(validators=[Length(6, 20, message='请输入正确格式的密码！')])
    remember = IntegerField()


# 修改密码表单验证
class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6, 20, message='请输入正确格式的旧密码！')])
    newpwd = StringField(validators=[Length(6, 20, message='请输入正确格式的新密码！')])
    newpwd2 = StringField(validators=[EqualTo('newpwd', message='确认密码必须和新密码一致！')])


# 修改邮箱表单验证类
class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确格式的新邮箱！')])
    captcha = StringField(validators=[Length(min=6, max=6, message='请输入正确长度的验证码！')])

    def validate_captcha(self, field):
        captcha = field.data  # 获取用户输入的验证码
        email = self.email.data
        captcha_cache = zlcache.get(email)  # 获取缓存中的验证码
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError('验证码有误！')

    def validate_email(self, field):
        email = field.data
        user = g.cms_user
        if user.email == email:
            raise ValidationError('不能修改位旧的邮箱！')
