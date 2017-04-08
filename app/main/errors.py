# coding: utf-8
# Created by leo on 17-4-8.
"""
错误处理
"""
from flask import render_template
from . import main

# 注意 app_errorhandler 是全局的


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


