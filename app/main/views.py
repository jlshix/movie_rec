# coding: utf-8
# Created by leo on 17-4-8.
"""
main 蓝本的视图
"""
from . import main
from flask import render_template


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/user/<name>', methods=['GET', 'POST'])
def user(name):
    return 'Hello {}'.format(name)