# !/usr/bin/env/python
# !-*-coding:utf-8 -*-
# !@Time     :2018/10/15  16:49
# !@Author   :Lening Wu
# !@File     models.py
# 数据模型

import password as password
import username as username

from nowstagram import db   # 导入数据库控制
import random


class User(db.Model):   # 对用户数据模型进行定义  和数据库想关联
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 对用户的ID进行设置
    username = db.Column(db.String(80), unique=True)  # 用户名为字符串
    password = db.Column(db.String(32))
    head_url = db.Column(db.String(256))

    def __init__(self, username, password):
        self.username = username  # 名字和密码都是外面传进来的，图片是从牛客网上抓取的
        self.password = password
        self.head_url = 'http://images.nowcoder.com/head/' + str(random.randint(0, 100)) + 'm.png'

    def __repr__(self):  # 表达用户
        return '<User %d %s>' % (self.id , self.username)
