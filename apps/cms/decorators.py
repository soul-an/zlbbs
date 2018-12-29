# encoding: utf-8
# decorators.py by Anderson Huang at 2018/12/25 10:46
from flask import session, redirect, url_for, g
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


# 权限验证装饰器，保证具有该权限才能访问该页面
def permission_required(permission):
    def outter(func):
        @wraps(func)
        def inner(*args, **kwargs):
            user = g.cms_user
            if user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                return redirect(url_for('cms.index'))  # 没有权限就重定向回主页

        return inner

    return outter
