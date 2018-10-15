#!-*-coding:utf-8 -*-
# 放导出信息


from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('app.conf')

from nowstagram import views, models
