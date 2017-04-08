# coding: utf-8
# Created by leo on 17-4-8.
"""
数据库模型
"""
from . import db
from flask_login import UserMixin
from . import lm


class User(db.Model, UserMixin):
    """
    用户模型 继承于数据库模型和 flask-login 的用户模型
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))

    # def __init__(self, name, email, password):
    #     self.name = name,
    #     self.email = email,
    #     self.password = password

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<User %r>' % self.name


@lm.user_loader
def load_user(user_id):
    """
    用户回调函数
    :param user_id: user_id
    :return: user
    """
    return User.query.get(int(user_id))
