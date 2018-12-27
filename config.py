# encoding: utf-8
# config.py by Anderson Huang at 2018/12/24 11:18
import os

"""
配置文件
"""

SECRET_KEY = os.urandom(24)   # 设置随机的SECRET_KEY

HOSTNAME = '192.168.1.114'
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

CMS_USER_ID = 'ahijdnknj'  # 随意设置cms用户的id字串
