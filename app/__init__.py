# coding: utf-8
# Created by leo on 17-4-8.
"""
主程序
供 run.py 调用返回实例
"""

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

bs = Bootstrap()
db = SQLAlchemy()
mail = Mail()

lm = LoginManager()
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

    from main import main as main_bp
    app.register_blueprint(main_bp)

    from auth import auth as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')     # 加前缀

    return app
