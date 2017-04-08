# coding: utf-8
# Created by leo on 17-4-8.
"""
主蓝本
用于电影展示相关功能
"""

from flask import Blueprint

main = Blueprint('main', __name__)

import views, errors

