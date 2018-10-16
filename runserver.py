#!/usr/bin/env/python
# !-*-coding:utf-8 -*-
# !@Time     :2018/10/15  16:04
# !@Author   :Lening Wu
# !@File    runserver.py
# 启动服务器

from nowstagram import app

if __name__ == '__main__':
    app.run(debug=True)


