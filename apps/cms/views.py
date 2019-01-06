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
    jsonify,
)
from .forms import (
    LoginForm,
    ResetpwdForm,
    ResetEmailForm,
    AddBannerForm,
    UpdateBannerForm,
)
from ..models import BannerModel
from .models import CMSUser, CMSPermission
from .decorators import login_required, permission_required
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


# 帖子管理模块视图
@bp.route('/posts/')
@login_required
@permission_required(CMSPermission.POSTER)
def posts():
    return render_template('cms/cms_posts.html')


# 评论管理模块驶入
@bp.route('/comments/')
@login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    return render_template('cms/cms_comments.html')


# 板块管理模块视图
@bp.route('/boards/')
@login_required
@permission_required(CMSPermission.BOARDER)
def boards():
    return render_template('cms/cms_boards.html')


# 前台用户管理模块视图
@bp.route('/fusers/')
@login_required
@permission_required(CMSPermission.FRONTUSER)
def fusers():
    return render_template('cms/cms_fusers.html')


# CMS用户管理视图
@bp.route('/cusers/')
@login_required
@permission_required(CMSPermission.CMSUSER)
def cusers():
    return render_template('cms/cms_cusers.html')


# CMS组管理视图
@bp.route('/croles/')
@login_required
@permission_required(CMSPermission.ALL_PERMISSION)
def croles():
    return render_template('cms/cms_croles.html')


# CMS轮播图管理视图
@bp.route('/banners/')
@login_required
def banners():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()  # 获取所有的轮播图,降序排列
    return render_template('cms/cms_banners.html', banners=banners)


# cms添加轮播图视图
@bp.route('/abanner/', methods=['POST'])
@login_required
def abanner():
    form = AddBannerForm(request.form)  # 验证
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data

        banner = BannerModel(name=name, image_url=image_url, link_url=link_url, priority=priority)
        db.session.add(banner)  # 保存
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


# cms编辑更新轮播图视图
@bp.route('/ubanner/', methods=['POST'])
@login_required
def ubanner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data

        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个轮播图！')
    else:
        return restful.params_error(message=form.get_error())


# cms删除轮播图视图函数
@bp.route('/dbanner/', methods=['POST'])
@login_required
def dbanner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error(message='请输入轮播图id！')

    banner = BannerModel.query.get(banner_id)
    if not banner:
        return restful.params_error(message='没有这个轮播图！')

    db.session.delete(banner)
    db.session.commit()

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
