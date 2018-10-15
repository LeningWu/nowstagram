#!/usr/bin/env/python
# !-*-coding:utf-8 -*-
# !@Time     :2018/10/15  16:05
# !@Author   :Lening Wu
# !@File     .py
# 把视图写在这里 页面

from nowstagram import app


@app.route('/')
def index():
    return 'hello'
