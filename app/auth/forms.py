# coding: utf-8
# Created by leo on 17-4-8.
"""
表单
包括登录表单 注册表单等
"""
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(Form):
    """
    登录表单 包括邮箱/密码/是否记住
    """
    email = StringField('email', validators=[DataRequired(), Email(), Length(1, 64)])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me ?')
    submit = SubmitField('Login')


class RegisterForm(Form):
    """
    注册表单 包括邮箱/用户名/密码/密码确认
    """
    email = StringField('email', validators=[DataRequired(), Email(), Length(1, 64)])
    name = StringField('nickname', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('password', validators=[DataRequired()])
    confirm = PasswordField('confirm password', validators=[
        DataRequired(), EqualTo('password', 'password not match')
    ])
    submit = SubmitField('Register')
