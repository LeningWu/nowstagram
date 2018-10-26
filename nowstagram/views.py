#!/usr/bin/env/python
# !-*-coding:utf-8 -*-
# !@Time     :2018/10/15  16:05
# !@Author   :Lening Wu
# !@File     .py
# 视图
# import password

from nowstagram import app
from nowstagram.models import Image, User, db
from flask import render_template, redirect, request, flash, get_flashed_messages
import random, hashlib
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/')  # 首页
def index():
    images = Image.query.order_by('id desc').limit(10).all()
    return render_template('index.html', images=images)


@app.route('/image/<int:image_id>')
def image(image_id):
    image=Image.query.get(image_id)
    if image == None:
        return redirect('/')
    return render_template('pageDetail.html', image=image)


@app.route('/profile/<int:user_id>')  # 用户个人页面
@login_required   # 加权限，用户要访问个人页必须要登录
def profile(user_id):
    user = User.query.get(user_id)
    if user == None:
        return redirect('/')
    return render_template('profile.html', user=user)


@app.route('/regloginpage/')  # 注册页面
def regloginpage():
    msg = ''
    for m in get_flashed_messages(with_categories=False, category_filter=['reglogin']):
        msg = msg + m
    return render_template('login.html', msg=msg)


def redirect_with_msg(target, msg, category):  # target跳转的页面
    if msg != None:
        flash(msg, category=category)
    return redirect(target)


@app.route('/reg/', methods={'post', 'get'})
def reg():
    # request.args 参数
    # request.form 提交过来的
    # strip去前后空格
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()

    # 如果发现用户名已经被注册，就返回到注册页上面
    user = User.query.filter_by(username=username).first()

    if username == '' or password == '':
       return redirect_with_msg('/regloginpage/', u'用户名或密码不能为空', 'reglogin')
    if user != None:
       return redirect_with_msg('/regloginpage/', u'用户名已存在', 'reglogin')

    # 更多判断
    # 对新注册用户密码做加盐的MD5加密
    salt = '.'.join(random.sample('01234567890abcdefghigABCDEFGHI', 10))  # 加盐加密
    m = hashlib.md5()
    m.update((password+salt).encode("utf8"))  # 在python3.5中在哈希之前必须要重新进行编码，用utf8要不然会报错
    password = m.hexdigest()  # 生成16进制的新密码
    user = User(username, password, salt)  # 把新注册的用户写入数据库
    db.session.add(user)
    db.session.commit()

    logout_user(user)  # 自动登录，登录状态

    return redirect('/')  # 返回首页


@app.route('/logout/')  # 登出
def logout():
    logout_user()
    return redirect('/')








