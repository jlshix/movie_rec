# coding: utf-8
# Created by leo on 17-4-8.
"""
用户验证蓝本 包括注册登录等
"""
from flask import Blueprint

auth = Blueprint('auth', __name__)

import views
