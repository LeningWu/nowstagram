# !/usr/bin/env/python
# !-*-coding:utf-8 -*-
# !@Time     :2018/10/15  16:49
# !@Author   :Lening Wu
# !@File     __init__.py
# 模块导出初始化


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')   # 可以在html文件中使用jinja的break语句
#  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config.from_pyfile('app.conf')
app.secret_key = 'nowcoder'
db = SQLAlchemy(app)
login_manager = LoginManager(app)  # 登录初始化
login_manager.login_view = '/regloginpage/'  # 已存在用户要进入个人主页，如果没登录的话自动跳入登录界面

from nowstagram import views, models