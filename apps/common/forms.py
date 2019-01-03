# encoding: utf-8
# forms.py by Anderson Huang at 2018/12/24 11:29
from wtforms import StringField
from wtforms.validators import regexp, InputRequired
from apps.forms import BaseForm  # 导入和继承基础表单验证类
import hashlib

"""
前台表单验证
"""


# 短信验证码验证表单类
class SMSCaptchaForm(BaseForm):
    salt = 'hihasiyfbfwe&($^*&hunggfaM'  # 加盐
    telephone = StringField(validators=[regexp(r'1[345789]\d{9}')])
    timestamp = StringField(validators=[regexp(r'\d{13}')])
    sign = StringField(validators=[InputRequired()])

    def validate(self):
        result = super(SMSCaptchaForm, self).validate()
        if not result:
            return False

        telephone = self.telephone.data
        timestamp = self.timestamp.data
        sign = self.sign.data
        print('客户端提交的sign: ', sign)

        # md5(timestamp+telephone+salt)  加密
        # md5函数必须传递一个bytes类型的字符串进去
        sign2 = hashlib.md5((timestamp + telephone + self.salt).encode(
            'utf-8')).hexdigest()  # hexdigest函数返回摘要，作为十六进制数据字符串值
        print('服务器生成的sign: ', sign2)

        if sign == sign2:
            return True
        else:
            return False
