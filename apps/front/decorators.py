# encoding: utf-8
# decorators.py by Anderson Huang at 2019/1/7 21:38
from functools import wraps
from flask import session, redirect, url_for

import config


# 必须登录
def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if config.FRONT_USER_ID in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('front.signin'))

    return inner
