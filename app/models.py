# coding: utf-8
# Created by leo on 17-4-8.
"""
数据库模型
"""
from . import db, lm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


class User(UserMixin, db.Model):
    """
    用户模型 继承于数据库模型和 flask-login 的用户模型
    """
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        pasword 属性只有 setter 没有 getter
        :return: Error
        """
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        """
        设置 password 散列值
        :param password: password
        :return: None
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        验证密码
        :param password: 输入的密码
        :return: bool
        """
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        """
        生成确认令牌 默认过期时间为1小时
        :param expiration: 过期时间
        :return: token
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        """
        令牌确认，更改 confirmed 字段
        :param token: token
        :return: bool
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

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
