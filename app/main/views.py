# coding: utf-8
# Created by leo on 17-4-8.
"""
main 蓝本的视图
"""
from . import main
from flask import render_template


@main.route('/', methods=['GET', 'POST'])
def index():
    """
    主页 待完善
    :return: render
    """
    return render_template('index.html')


@main.route('/user/<int:id>', methods=['GET', 'POST'])
def user(id):
    """
    用户页面 待完善
    :param name:
    :return:
    """
    return 'Hello {}'.format(id)