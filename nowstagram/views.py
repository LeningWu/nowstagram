#!/usr/bin/env/python
# !-*-coding:utf-8 -*-
# !@Time     :2018/10/15  16:05
# !@Author   :Lening Wu
# !@File     .py
# 视图

from nowstagram import app


@app.route('/')
def index():
    return 'hello'
