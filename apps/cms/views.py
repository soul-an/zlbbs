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
from .forms import LoginForm, ResetpwdForm, ResetEmailForm
from .models import CMSUser
from .decorators import login_required
from exts import db, mail
from flask_mail import Message
from utils import restful, zlcache
import config
import string
import random

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


# 测试发送邮件视图
@bp.route('/email/')
@login_required
def send_email():
    message = Message('邮件发送', recipients=['huanganfa66@163.com'], body='测试')
    mail.send(message)
    return '邮件已发送成功！'


# 发送邮件验证码视图
@bp.route('/email_captcha/')
@login_required
def email_captcha():
    # /email_captcha/?email=xxx.@qq.com 获取到发送邮箱
    email = request.args.get('email')
    if not email:
        return restful.params_error('请传递邮箱参数！')

    # 随机生成6位验证码字串,大小写字母加上0-9数字
    source = list(string.ascii_letters)
    source.extend(map(lambda x: str(x), range(0, 10)))
    captcha = "".join(random.sample(source, 6))

    # 给获取到的新的邮箱发送邮件验证码
    message = Message('知了论坛邮箱验证码', recipients=[email], body='你的验证码是：%s' % captcha)
    try:
        mail.send(message)
    except:
        return restful.server_error()
    zlcache.set(email, captcha)  # 添加验证码缓存
    return restful.success()


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


# 修改邮箱类视图
class ResetEmailView(views.MethodView):
    decorators = [login_required]  # 保证用户登陆

    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            user = g.cms_user
            user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))
