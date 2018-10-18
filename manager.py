# !-*-coding:utf-8 -*-
# 脚本数据

import random
from flask_script import Manager
from nowstagram import app, db
from nowstagram.models import Image, Comment, User

manager = Manager(app)


def get_image_url():
    return 'http://images.nowcoder.com/head/' + str(random.randint(0, 100)) + 'm.png'


@manager.command
def init_database():  # 有100个用户，每个用户三张图片，每个图片三个评论
    db.drop_all()
    db.create_all()
    for i in range(0, 100):
        db.session.add(User('User' + str(i), 'a'+str(i)))  # 对user进行写入
        for j in range(0, 3):
            db.session.add(Image(get_image_url(), i+1))  # 对图片数据库进行写入
            for k in range(0, 3):
                db.session.add(Comment('This is a comment' + str(k), 1+3*i+j, i+1))

    db.session.commit()  # 提交事务


if __name__ == '__main__':
    manager.run()