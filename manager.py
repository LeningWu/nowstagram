# !-*-coding:utf-8 -*-
# 脚本数据
from nowstagram import app , db
from flask_script import Manager

manager = Manager(app)


@manager.command
def init_database():
    db.drop_all()
    db.create_all()


if __name__ == '__name__':
    manager.run()