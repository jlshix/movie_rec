# coding: utf-8
# Created by leo on 17-4-8.
"""
数据库模型
"""
from . import db, lm
from mongoengine import (StringField, IntField, BooleanField, DateTimeField,
                         SequenceField, ListField, ReferenceField)
from bson import ObjectId
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from config import LIKE_TYPE, WATCH_TYPE


class User(UserMixin, db.Document):
    """
    用户模型 继承于数据库模型和 flask-login 的用户模型
    """
    uid = SequenceField()
    name = StringField(max_length=64, unique=True, required=True)
    email = StringField(max_length=64, unique=True, required=True)
    password_hash = StringField(max_length=128)
    confirmed = BooleanField(default=False)
    since = DateTimeField(default=datetime.utcnow())
    gender = BooleanField(default=True)
    interests = ListField(StringField(max_length=64))

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
        return s.dumps({'confirm': str(self.id)})

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
        if data.get('confirm') != str(self.id):
            return False
        self.confirmed = True
        self.save()
        return True

    def __repr__(self):
        return '<User %r>' % self.name


@lm.user_loader
def load_user(user_id):
    """
    用户回调函数
    :param user_id: user_id
    :return: user
    """
    return User.objects(id=ObjectId(user_id)).first()


class Like(db.Document):
    """
    用户喜欢的
    type 包括 电影 影人
    name 为名称
    value 为 id
    """
    user = ReferenceField(User)
    type = StringField(max_length=16, choices=LIKE_TYPE)
    name = StringField()
    value = StringField()
    dt = DateTimeField(default=datetime.utcnow())


class Rating(db.Document):
    """
    评论
    包括电影id 标题 内容
    """
    user = ReferenceField(User)
    rating = IntField(min_value=0, max_value=10)
    mid = StringField(max_length=16)
    title = StringField(max_length=64)
    content = StringField()
    dt = DateTimeField(default=datetime.utcnow())


class Wt(db.Document):
    """
    想看 在看 看过
    """
    user = ReferenceField(User)
    type = StringField(max_length=16, choices=WATCH_TYPE)
    name = StringField()
    value = StringField(max_length=64)
    dt = DateTimeField(default=datetime.utcnow())