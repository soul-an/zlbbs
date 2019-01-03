# encoding: utf-8
# views.py by Anderson Huang at 2018/12/24 11:28
from flask import (
    Blueprint,
    views,
    render_template,
    request
)
from .forms import SignupForm
from utils import restful, safeutils
from .models import FrontUser
from exts import db

bp = Blueprint('front', __name__)


# 主页视图
@bp.route('/')
def index():
    return render_template('front/front_index.html')


# 测试页面视图
@bp.route('/test/')
def front_test():
    return render_template('front/front_test.html')


# 注册类视图
class SignupView(views.MethodView):
    def get(self):
        # 跳转到之前的页面,如果存在的话
        return_to = request.referrer
        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
            return render_template('front/front_signup.html', return_to=return_to)
        else:
            return render_template('front/front_signup.html')

    def post(self):
        # 验证表单
        form = SignupForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data

            # 创建新的前台用户
            user = FrontUser(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            print(form.get_error())  # 打印出错误信息
            return restful.params_error(message=form.get_error())


bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))
