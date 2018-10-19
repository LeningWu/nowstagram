# !/usr/bin/env/python
# !-*-coding:utf-8 -*-
# !@Time     :2018/10/15  16:49
# !@Author   :Lening Wu
# !@File     __init__.py
# 模块导出


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')   # 可以在html文件中使用jinja的break语句，
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


from nowstagram import views, models