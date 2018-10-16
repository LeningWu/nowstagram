# !/usr/bin/env/python
# !-*-coding:utf-8 -*-
# !@Time     :2018/10/15  16:49
# !@Author   :Lening Wu
# !@File     __init__.py
# 模块导出


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('app.conf')
db = SQLAlchemy(app)


from nowstagram import views, models
