# coding: utf-8
# Created by leo on 17-4-8.
"""
配置文件
"""
import os
base_dir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """
    配置类 所有无父类的默认继承 object
    """
    DEBUG = True
    # 秘钥从环境变量获取或生成
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(base_dir, 'app.db')