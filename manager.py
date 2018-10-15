# !-*-coding:utf-8 -*-
# 脚本写这里
from nowstagram import app
from flask_script import Manager

manager = Manager(app)

if __name__ == '__name__':
    manager.run()