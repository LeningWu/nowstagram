#!/usr/bin/env/python
# !-*-coding:utf-8 -*-
# !@Time     :2018/10/15  16:05
# !@Author   : Lening Wu
# !@File     views.py
import os
import uuid

from nowstagram import app
from nowstagram.models import Image, User, db
from flask import render_template, redirect, request, flash, get_flashed_messages, send_from_directory
import random, hashlib, json
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/')  # 首页
def index():
    images = Image.query.order_by('id desc').limit(10).all()
    return render_template('index.html', images=images)


@app.route('/image/<int:image_id>')
def image(image_id):
    image = Image.query.get(image_id)
    if image == None:
        return redirect('/')
    return render_template('pageDetail.html', image=image)


@app.route('/profile/<int:user_id>')  # 用户个人页面
@login_required  # 加权限，用户要访问个人页必须要登录
def profile(user_id):
    user = User.query.get(user_id)
    if user == None:
        return redirect('/')
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=1, per_page=3, error_out=False)  # 对用户业进行分页，每页显示三张图片
    return render_template('profile.html', user=user, images=paginate.items, has_next=paginate.has_next)


# ajix请求，不刷新页面来进行页面更新，类似于不刷新页面的情况下的看更多图片
@app.route('/profile/images/<int:user_id>/<int:page>/<int:per_page>/')
def user_images(user_id, page, per_page):
    paginate = Image.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)

    map = {'has_next': paginate.has_next}  # 不停的点击更多，图片加载完成以后更多的按钮要消失
    images = []
    for image in paginate.items:
        imgvo = {'id': image.id, 'url': image.url, 'comment_count': len(image.comments)}
        images.append(imgvo)

    map['images'] = images
    return json.dumps(map)


@app.route('/regloginpage/')  # 注册页面
def regloginpage():
    msg = ''
    for m in get_flashed_messages(with_categories=False, category_filter=['reglogin']):
        msg = msg + m
    return render_template('login.html', msg=msg, next=request.values.get('next'))  # 把next传进去用来登录后直接进入个人页面


def redirect_with_msg(target, msg, category):  # target跳转的页面
    if msg != None:
        flash(msg, category=category)
    return redirect(target)


@app.route('/login/', methods={'post', 'get'})  # 登录页面
def login():
    username = request.values.get('username').strip()
    password = request.values.get('password').strip()

    if username == '' or password == '':
        return redirect_with_msg('/regloginpage/', u'用户名或密码不能为空', 'reglogin')

    user = User.query.filter_by(username=username).first()  # 看登录的用户名存不存在
    if user == None:
        return redirect_with_msg('/regloginpage/', u'用户名不存在', 'reglogin')

    m = hashlib.md5()
    m.update((password + user.salt).encode("utf8"))
    if (m.hexdigest() != user.password):
        return redirect_with_msg('/regloginpage/', u'密码错误', 'reglogin')

    login_user(user)  # 告诉框架用户已经登录

    next = request.values.get('next')
    if next != None and next.startswith('/'):
        return redirect(next)

    return redirect('/')


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
    m.update((password + salt).encode("utf8"))  # 在python3.5中在哈希之前必须要重新进行编码，用utf8要不然会报错
    password = m.hexdigest()  # 生成16进制的新密码
    user = User(username, password, salt)  # 把新注册的用户写入数据库
    db.session.add(user)
    db.session.commit()

    login_user(user)  # 自动登录，登录状态

    next = request.values.get('next')
    if next != None and next.startswith('/'):
        return redirect(next)

    return redirect('/')  # 返回首页


@app.route('/logout/')  # 登出
def logout():
    logout_user()
    return redirect('/')  # 退出登录回到首页


def save_to_local(file, file_name):  # 图片保存本地
    # save_dir = app.config['UPLOAD_DIR']
    save_dir = '/Users/wulening/Desktop/'
    file.save(os.path.join(save_dir, file_name))
    return '/image/' + file_name


@app.route('/image/<image_name>')
def view_image(image_name):
    return send_from_directory(app.config['UPLOAD_DIR'], image_name)


# 上传图片
@app.route('/upload/', methods={'POST'})  # 上传的入口必须用post请求 提交过来一张图片
@login_required  # 加权限，必须要登录
def upload():
    # if current_user.is_authenticated():
    file = request.files['file']  # 保存上传文件
    if file.filename.find('.') > 0:  # 鉴定文件名是否符合要求
        file_ext = file.filename.rsplit('.', 1)[1].strip().lower()
    if file_ext in app.config['ALLOWED_EXT']:
        file_name = str(uuid.uuid1()).replace('-', '') + '.' + file_ext  # 随机值
        url = save_to_local(file, file_name)

        if url != None:
            db.session.add(Image(url, current_user.id))
            db.session.commit()

    return redirect('/profile/%d' % current_user.id)
