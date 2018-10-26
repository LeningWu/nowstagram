# !/usr/bin/env/python
# !-*-coding:utf-8 -*-
# !@Time     :2018/10/15  16:49
# !@Author   :Lening Wu
# !@File     models.py
# 数据模型

import random
from datetime import datetime
from nowstagram import db, login_manager # 导入数据库控制


class Comment(db.Model):   # 评论类
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(1024))
    imang_id = db.Column(db.Integer, db.ForeignKey('image.id'))  # 这里吧image_id写成了inang_id 要注意构造函数那里也要修改
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Integer, default=0)  # 0正常 1删除
    user = db.relationship('User')

    def __init__(self, content, image_id, user_id):
        self.content = content
        self.imang_id = image_id   # 注意！！！！！！
        self.user_id = user_id

    def __repr__(self):  # 表达评论
        return '<Comment %d %s>' % (self.id, self.content)


class Image(db.Model):  # 图片类
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url = db.Column(db.String(512))  # type:
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime)
    comments = db.relationship('Comment')

    def __init__(self, url, user_id):
        self.url = url
        self.user_id = user_id
        self.created_date = datetime.now()

    def __repr__(self):  # 表达图片
        return '<Image %d %s>' % (self.id, self.url)


class User(db.Model):   # 对用户数据模型进行定义  和数据库想关联
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 对用户的ID进行设置
    username = db.Column(db.String(80), unique=True)  # 用户名为字符串
    password = db.Column(db.String(32))
    salt = db.Column(db.String(32))  # 对密码加盐加密
    head_url = db.Column(db.String(256))
    images = db.relationship('Image', backref='user', lazy='dynamic')  # backref是为了让图片和USER相关联，可以从图片查询到User

    def __init__(self, username, password, salt=''):
        self.username = username  # 名字和密码都是外面传进来的，图片是从牛客网上抓取的
        self.password = password
        self.salt = salt
        self.head_url = 'http://images.nowcoder.com/head/' + str(random.randint(0, 100)) + 'm.png'

    def __repr__(self):  # 表达用户
        return '<User %d %s>' % (self.id , self.username)

    @property
    def is_authenticate(self):  # 只要是登陆过的都认为是激活的
        return True

    @property
    def is_active(self):  # 只要是登陆过的都认为是激活的
        return True

    @property
    def is_anonymous(self):  # 是不是匿名的
        return False

    def get_id(self):  # 获取ID
        return self.id


@login_manager.user_loader  # 用户ID直接加载用户
def load_user(user_id):
    return User.query.get(user_id)
