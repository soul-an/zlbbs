# encoding: utf-8
# forms.py by Anderson Huang at 2018/12/26 12:00
from wtforms import Form


# 基础的表单验证类
class BaseForm(Form):
    def get_error(self):
        message = self.errors.popitem()[1][0]  # 需要返回什么信息视具体情况而定
        return message
