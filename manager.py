# !-*-coding:utf-8 -*-
# 脚本数据

import random
import unittest
from flask_script import Manager
from sqlalchemy import or_, and_
from nowstagram import app, db
from nowstagram.models import Image, Comment, User

manager = Manager(app)


def get_image_url():
    return 'http://images.nowcoder.com/head/' + str(random.randint(0, 100)) + 'm.png'


@manager.command  # 跑测试用例
def run_test():
    tests = unittest.TestLoader().discover('./')
    unittest.TextTestRunner().run(tests)


@manager.command
def init_database():  # 有100个用户，每个用户三张图片，每个图片三个评论
    db.drop_all()
    db.create_all()
    for i in range(0, 100):
        db.session.add(User('User' + str(i+1), 'a'+str(i)))  # 对user进行写入
        for j in range(0, 3):
            db.session.add(Image(get_image_url(), i+1))  # 对图片数据库进行写入
            for k in range(0, 3):
                db.session.add(Comment('This is a comment' + str(k), 1+3*i+j, i+1))
    db.session.commit()  # 提交往表里写数据的命令一定记得是在第一个for循环里！！！！！！！要不然没法写入

    # 数据库更新
    for i in range(50, 100, 2):  # 50到100的偶数的用户名进行修改
        user = User.query.get(i)
        user.username = '[New1]' + user.username

    User.query.filter_by(id=51).update({'username':'[New2]'})  # 第二种更新
    db.session.commit()

    # 数据库中删除一些评论
    for i in range(50, 100, 2):  # 编号50到100的双数编号评论删除
        comment = Comment.query.get(i+1)
        db.session.delete(comment)
    db.session.commit()

    # 数据库数据查询
    print(1, User.query.all())  # 查询所有
    print(2, User.query.get(3))  # 查询指定数据
    print(3, User.query.filter_by(id=5).first())  # 查询排第五的
    print(4, User.query.order_by(User.id.desc()).offset(1).limit(2).all())  # id的降序，排完序列后offset偏移一个，在打出两个limit
    print(5, User.query.filter(User.username.endswith('0')).limit(3).all())  # 打出结尾是0的，但limit3个，只打出来三个
    print(6, User.query.filter(or_(User.id == 88, User.id == 99)).all())
    print(7, User.query.filter(and_(User.id > 88, User.id < 93)).all())
    print(8, User.query.filter(and_(User.id > 88, User.id < 93)).first_or_404())
    print(9, User.query.order_by(User.id.desc()).paginate(page=1, per_page=10).items)  # 给数据库数据逆序分页，一页10个人
    # 一对多查询
    user = User.query.get(1)
    print(10, user.images)  # 把user1用户的图片全部查询出来，因为有关联，和外键关联

    image = Image.query.get(1)
    print(11, image, image.user)  # 从图片来查找用户，在models里面要进行一下关联


if __name__ == '__main__':
    manager.run()