# encoding: utf-8
# hooks.py by Anderson Huang at 2018/12/25 14:31
from .views import bp
from flask import session, g
from .models import CMSUser
import config

"""
存放钩子函数
"""


# 钩子函数，线程隔离的g对象，实现cms用户名渲染
@bp.before_request
def before_request():
    if config.CMS_USER_ID in session:
        user_id = session.get(config.CMS_USER_ID)
        user = CMSUser.query.get(user_id)
        if user:
            g.cms_user = user
