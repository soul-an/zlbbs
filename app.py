from flask import Flask
from apps.cms import bp as cms_bp
from apps.front import bp as front_bp
from apps.common import bp as common_bp
from apps.ueditor import bp as ueditor_bp
from exts import db, mail, alidayu
from flask_wtf import CSRFProtect
import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    app.register_blueprint(cms_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(ueditor_bp)

    db.init_app(app)
    mail.init_app(app)
    alidayu.init_app(app)  # 初始化阿里大于api对象

    CSRFProtect(app)  # 添加CSRF（跨站域请求伪造cross site request forgery）保护，防止漏洞

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8000)
