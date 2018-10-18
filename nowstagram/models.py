# !/usr/bin/env/python
# !-*-coding:utf-8 -*-
# !@Time     :2018/10/15  16:49
# !@Author   :Lening Wu
# !@File     models.py
# 数据模型

import random
from datetime import datetime
from nowstagram import db  # 导入数据库控制


class Comment(db.Model):   # 评论类
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(1024))
    imang_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Integer, default=0)  # 0正常 1删除
    user = db.relationship('User')

    def __init__(self, content, image_id, user_id):
        self.content = content
        self.imang_id = image_id
        self.user_id = user_id

    def __repr__(self):  # 表达评论
        return '<Comment %d %s>' % (self.id, self.content)


class Image(db.Model):  # 图片类
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(512))  # type:
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime)
    comments = db.relationship('Comment')

    def __init__(self , url, user_id):
        self.url = url
        self.user_id = user_id
        self.created_date = datetime.now()

    def __repr__(self):  # 表达图片
        return '<Image %d %s>' % (self.id, self.url)


class User(db.Model):   # 对用户数据模型进行定义  和数据库想关联
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 对用户的ID进行设置
    username = db.Column(db.String(80), unique=True)  # 用户名为字符串
    password = db.Column(db.String(32))
    head_url = db.Column(db.String(256))
    images = db.relationship('Image')

    def __init__(self, username, password):
        self.username = username  # 名字和密码都是外面传进来的，图片是从牛客网上抓取的
        self.password = password
        self.head_url = 'http://images.nowcoder.com/head/' + str(random.randint(0, 100)) + 'm.png'

    def __repr__(self):  # 表达用户
        return '<User %d %s>' % (self.id , self.username)
