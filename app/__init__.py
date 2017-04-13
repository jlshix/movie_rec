# coding: utf-8
# Created by leo on 17-4-8.
"""
主程序
供 run.py 调用返回实例
"""

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, AnonymousUserMixin
from flask_mail import Mail
from flask_pymongo import PyMongo


class Anonymous(AnonymousUserMixin):
    """
    暂时写这里 放在 models 会让导入变乱
    匿名用户类 增加id与nickname属性，用于判断
    """
    def __init__(self):
        self.id = 0
        self.name = 'Guest'
bs = Bootstrap()
db = SQLAlchemy()
mail = Mail()
mg = PyMongo()

lm = LoginManager()
lm.anonymous_user = Anonymous
lm.session_protection = 'strong'
lm.login_view = 'auth.login'


def create_app(conf=None):
    """
    工厂函数，返回实例
    :param conf: 配置
    :return: app
    """
    app = Flask(__name__)
    app.config.from_object(conf)
    bs.init_app(app)
    db.init_app(app)
    lm.init_app(app)
    mail.init_app(app)
    mg.init_app(app, config_prefix='MONGO1')

    from main import main as main_bp
    app.register_blueprint(main_bp)

    from auth import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')     # 加前缀

    from api import api as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
