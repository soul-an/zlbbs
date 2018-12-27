# encoding: utf-8
# forms.py by Anderson Huang at 2018/12/24 11:29
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Email, InputRequired, Length, EqualTo
from apps.forms import BaseForm   # 导入和继承基础表单验证类

"""
表单验证
"""


# 登陆表单验证
class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确的邮箱'), InputRequired(message='请输入邮箱地址')])
    password = StringField(validators=[Length(6, 20, message='请输入正确的密码')])
    remember = IntegerField()


# 修改密码表单验证
class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6, 20, message='请输入正确格式的旧密码')])
    newpwd = StringField(validators=[Length(6, 20, message='请输入正确格式的新密码')])
    newpwd2 = StringField(validators=[EqualTo('newpwd', message='确认密码必须和新密码一致')])
