# coding: utf-8
# Created by leo on 17-4-8.
"""
辅助工具
"""

from app import mail
from flask_mail import Message
from flask import render_template
from threading import Thread
from flask import current_app


def send_async_email(msg):
    """
    异步发送邮件
    :param msg: 邮件内容
    :return: None
    """
    with current_app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    """
    发邮件
    :param to: 收件人
    :param subject: 主题
    :param template: 模板
    :param kwargs: 模板字段
    :return: thread
    """
    msg = Message(subject, recipients=[to], sender='471819708@qq.com')
    msg.body = render_template(template+'.txt', **kwargs)
    msg.html = render_template(template+'.html', **kwargs)
    thr = Thread(target=send_async_email, args=[msg])
    thr.start()
    return thr
