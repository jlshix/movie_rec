# coding: utf-8
# Created by leo on 17-4-8.
"""
配置文件
"""
import os
base_dir = os.path.abspath(os.path.dirname(__file__))
WATCH_TYPE = ['want', 'watching', 'watched']
LIKE_TYPE = ['movie', 'celebrity']


class Config(object):
    """
    配置类 所有无父类的默认继承 object
    """
    DEBUG = True
    # 秘钥从环境变量获取或生成
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)

    # mongoengine
    MONGODB_SETTINGS = {
        'db': 'mr'
    }

    # pymongo
    MONGO1_DBNAME = 'mr'

    # flask-mail 相关配置
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = '471819708'
    # MAIL_PASSWORD = 'xqbtqpzubfzlbjae'
    MAIL_PASSWORD = 'hfomwddcurnfbjfe'
    # MAIL_PASSWORD = "sjl'sqqno0x"
    MAIL_SUBJECT_PREFIX = '[Movie Rec]'
    MAIL_SENDER = 'Leo<471819708@qq.com>'
    ADMIN = MAIL_SENDER
