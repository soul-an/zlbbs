# encoding: utf-8
# restful.py by Anderson Huang at 2018/12/26 14:24
from flask import jsonify

"""
前端和后端通讯的规范，优化http状态码和返回的json数据
"""


class HttpCode(object):
    ok = 200
    unautherror = 401
    paramserror = 400
    servererror = 500


def restful_result(code, message, data):
    return jsonify({'code': code, 'message': message, 'data': data})


def success(message="", data=None):
    return restful_result(code=HttpCode.ok, message=message, data=data)


def unauth_error(message="", data=None):
    return restful_result(code=HttpCode.unautherror, message=message, data=data)


def params_error(message="", data=None):
    return restful_result(code=HttpCode.paramserror, message=message, data=data)


def server_error(message="", data=None):
    return restful_result(code=HttpCode.servererror, message=message or '服务器内部错误', data=data)
