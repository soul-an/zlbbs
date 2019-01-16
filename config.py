# encoding: utf-8
# config.py by Anderson Huang at 2018/12/24 11:18
import os

"""
配置文件
"""

SECRET_KEY = os.urandom(24)  # 设置随机的SECRET_KEY

HOSTNAME = '192.168.1.114'  # 链接远程mysql数据库
# HOSTNAME = '127.0.0.1'  # 链接本机mysql数据库
PORT = '3306'
DATABASE = 'zlbbs'
USERNAME = 'root'
PASSWORD = '19881214An'
# mysql+pymysql://root:19881214An@192.168.1.114:3306/flask_learn?charset=utf8
DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}" \
         "/{db}?charset=utf8".format(username=USERNAME, password=PASSWORD,
                                     host=HOSTNAME, port=PORT, db=DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

CMS_USER_ID = 'ahijdnknj'  # 随意设置cms后台用户的id字串
FRONT_USER_ID = 'ihisdfkjds'  # 随意设置front前台用户的id字串

# 发送者邮箱的服务器地址和邮箱配置参数，这里使用qq邮箱
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = '587'
MAIL_USE_TLS = True
MAIL_USERNAME = '773985366@qq.com'
MAIL_PASSWORD = 'sjvjkwmovrkzbdge'
MAIL_DEFAULT_SENDER = '773985366@qq.com'

# 阿里大于短信验证码相关配置参数
ALIDAYU_APP_KEY = '23709557'
ALIDAYU_APP_SECRET = 'd9e430e0a96e21c92adacb522a905c4b'
ALIDAYU_SIGN_NAME = '小饭桌应用'
ALIDAYU_TEMPLATE_CODE = 'SMS_68465012'

# UEditor相关配置
UEDITOR_UPLOAD_TO_QINIU = True
UEDITOR_QINIU_ACCESS_KEY = "wxQkXHCKUiApHFma-Q6exrQcTk9pEtLSU9w136ut"
UEDITOR_QINIU_SECRET_KEY = "55ChWSMN59xLNg6CvNQXrgVXmjxqRbljy3QzHuKi"
UEDITOR_QINIU_BUCKET_NAME = "zlbbs-qiniu1"
UEDITOR_QINIU_DOMAIN = "http://pl09sxlvg.bkt.clouddn.com/"

# flask-paginate分页器相关配置
PER_PAGE = 10  # 每页包含的帖子数量

# Celery相关配置
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'  # 本地Redis服务
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
# CELERY_RESULT_BACKEND = 'redis://192.168.1.114:6379/0'
# CELERY_BROKER_URL = 'redis://192.168.1.114:6379/0'
