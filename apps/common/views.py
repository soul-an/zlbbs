# encoding: utf-8
# views.py by Anderson Huang at 2018/12/24 11:28
from flask import Blueprint, request, make_response
from exts import alidayu
from utils import restful, zlcache
from utils.captcha import Captcha
from apps.common.forms import SMSCaptchaForm
from io import BytesIO

bp = Blueprint('common', __name__, url_prefix='/common')


# 短信验证码发送视图函数
# @bp.route('/sms_captcha/')
# def sms_captcha():
#     # ?telephone=xxx  ===>   /common/sms_capcha/xxx
#     telephone = request.args.get('telephone')
#     if not telephone:
#         return restful.params_error(message='请传入手机号码！')
#     captcha = Captcha.gene_text(number=6)  # 生成6位的验证码
#     if alidayu.send_sms(telephone, code=captcha):
#         return restful.success()
#     else:
#         # return restful.params_error(message='短信验证码发送失败！')
#         return restful.success()   # 为了方便开发，假设短信发送成功

# 短信验证码发送视图函数  加密功能改进版
@bp.route('/sms_captcha/', methods=['POST'])
def sms_captcha():
    # telephone
    # timestamp
    # md5(ts+telephone+salt)
    form = SMSCaptchaForm(request.form)
    if form.validate():
        telephone = form.telephone.data
        captcha = Captcha.gene_text(number=6)
        print('发送的短信验证码是：', captcha)  # 打印出短信验证码
        if alidayu.send_sms(telephone, code=captcha):
            zlcache.set(telephone, captcha)  # 将验证码缓存到memcached系统中
            return restful.success()
        else:
            # return restful.params_error(message='短信验证码发送失败！')
            zlcache.set(telephone, captcha)  # 这里是为了方便开发工作
            return restful.success()  # 为了方便开发，假设短信发送成功
    else:
        return restful.params_error(message='参数错误！')


# 图形验证码生成视图函数
@bp.route('/captcha/')
def graph_captcha():
    captcha, image = Captcha.gene_graph_captcha()
    print('图形验证码是：', captcha)  # 打印出图形验证码
    zlcache.set(captcha.lower(), captcha.lower())  # 把验证码添加到memcached缓存中
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp
