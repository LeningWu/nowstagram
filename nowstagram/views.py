#!/usr/bin/env/python
# !-*-coding:utf-8 -*-
# !@Time     :2018/10/15  16:05
# !@Author   :Lening Wu
# !@File     .py
# 视图

from nowstagram import app
from nowstagram.models import Image
from flask import render_template


@app.route('/')
def index():
    image = Image.query.order_by('id desc').limit(10).all()
    return render_template('index.html', images=images)
