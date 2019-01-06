# encoding: utf-8
# manage.py by Anderson Huang at 2018/12/24 13:45
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from exts import db
from app import create_app
from apps.cms import models as cms_models
from apps.front import models as front_models
from apps.models import BannerModel  # 轮播图模型

# 后台模型对象
CMSUser = cms_models.CMSUser
CMSRole = cms_models.CMSRole
CMSPermission = cms_models.CMSPermission

# 前台模型对象
FrontUser = front_models.FrontUser

app = create_app()

manager = Manager(app)

Migrate(app, db)
manager.add_command('db', MigrateCommand)


# 命令行创建cms用户函数
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_cms_user(username, password, email):
    user = CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print('CMS用户添加成功！')


# 命令行创建角色函数
@manager.command
def create_role():
    # 1.访问者（可以修改个人信息）
    visitor = CMSRole(name='访问者', desc='只能查看数据，不能修改')
    visitor.permissions = CMSPermission.VISITOR

    # 2.运营者（修改个人信息，管理帖子、管理评论、管理前台用户）
    operator = CMSRole(name='运营者', desc='管理帖子、管理评论、管理前台用户')
    operator.permissions = CMSPermission.VISITOR | CMSPermission.POSTER | CMSPermission.COMMENTER | CMSPermission.FRONTUSER

    # 3.管理员（拥有绝大部分权限）
    admin = CMSRole(name='管理员', desc='拥有本系统所有权限')
    admin.permissions = CMSPermission.VISITOR | CMSPermission.POSTER | CMSPermission.COMMENTER | CMSPermission.FRONTUSER | CMSPermission.CMSUSER

    # 4.开发者
    developer = CMSRole(name='开发者', desc='开发人员专用')
    developer.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor, operator, admin, developer])
    db.session.commit()
    print('CMS角色添加成功！')


# 命令行添加用户某一权限的函数
@manager.option('-e', '--email', dest='email')
@manager.option('-n', '--name', dest='name')
def add_user_to_role(email, name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print('用户添加到角色成功！')
        else:
            print('没有这个角色：%s' % role)
    else:
        print('没有这个用户：%s' % email)


# 命令行测试用户是否具有某一权限的函数
@manager.option('-n', '--name', dest='name')
@manager.option('-e', '--email', dest='email')
def test_permission(name, email):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        if name == '访问者':
            if user.has_permission(CMSPermission.VISITOR):
                print('这个用户有访问者权限！')
            else:
                print('这个用户没有访问者权限！')
        elif name == '运营者':
            if user.has_permission(CMSPermission.POSTER):
                print('这个用户有运营者权限！')
            else:
                print('这个用户没有运营者权限！')
        elif name == '管理员':
            if user.has_permission(CMSPermission.CMSUSER):
                print('这个用户有管理员权限！')
            else:
                print('这个用户没有管理员权限！')
        elif name == '开发者':
            if user.is_developer:
                print('这个用户有开发者权限！')
            else:
                print('这个用户没有开发者权限！')
    else:
        print('没有这个用户！')


# 命令行创建前台用户映射函数
@manager.option('-t', '--telephone', dest='telephone')
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_front_user(telephone, username, password):
    user = FrontUser(telephone=telephone, username=username, password=password)
    db.session.add(user)
    db.session.commit()
    print('FRON前台用户创建成功！')


if __name__ == '__main__':
    manager.run()
