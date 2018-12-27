# encoding: utf-8
# decorators.py by Anderson Huang at 2018/12/25 10:46
from flask import session, redirect, url_for
from functools import wraps
import config

"""
装饰器。
"""


# cms后台登陆限制，如果用户没有登陆，就会自动跳转到cms登陆页面
# 只有登陆成功，才会跳转到主页面
def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if config.CMS_USER_ID in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('cms.login'))

    return inner
