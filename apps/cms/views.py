# encoding: utf-8
# views.py by Anderson Huang at 2018/12/24 11:28
from flask import (
    Blueprint,
    views,
    render_template,
    request, session,
    redirect,
    url_for,
    g,
    jsonify)
from .forms import LoginForm, ResetpwdForm
from .models import CMSUser
from .decorators import login_required
from exts import db
from utils import restful
import config

bp = Blueprint('cms', __name__, url_prefix='/cms')


# cms后台主页视图函数
@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')  # 跳转到cms后台主页


# 注销视图函数
@bp.route('/logout/')
@login_required
def logout():
    del session[config.CMS_USER_ID]  # 删除session中的用户id字串
    return redirect(url_for('cms.login'))  # 返回登陆页面


# 个人详情页面视图函数
@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')


# 登录类视图
class LoginView(views.MethodView):

    def get(self, message=None):
        return render_template('cms/cms_login.html', message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data

            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.CMS_USER_ID] = user.id  # 指定用户id为固定的字串
                if remember:
                    # 如果设置session.permanent = True, 那么过期时间是31天
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                return self.get(message='邮箱或者密码错误')
        else:
            # print(form.errors)
            # message = form.errors.popitem()[1][0]  # 提取表单验证forms.py传递过来的消息
            message = form.get_error()  # 修改为使用父类的get_error()方法
            return self.get(message=message)


# 修改密码类视图
class ResetPwdView(views.MethodView):
    decorators = [login_required]  # 保证用户登陆

    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetpwdForm(request.form)  # 验证修改密码
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user  # 使用g对象传递用户对象
            if user.check_password(oldpwd):
                # 更新数据库中的密码
                user.password = newpwd
                db.session.commit()
                # 返回json数据
                # return jsonify({"code": 200, "message": ""})
                return restful.success()
            else:
                # return jsonify({"code": 400, "message": "旧密码输入错误"})
                return restful.params_error("旧密码错误")
        else:
            message = form.get_error()  # 使用父类的get_error()方法获取错误信息
            # return jsonify({"code": 400, "message": message})
            return restful.params_error(message)


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
