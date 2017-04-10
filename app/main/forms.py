# coding: utf-8
# Created by leo on 17-4-8.
"""
表格
"""

from flask_wtf import FlaskForm as Form
from wtforms import IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, AnyOf


class SearchForm(Form):
    """
    搜索
    """
    name = StringField('Name', validators=[Length(max=20)])
    submit = SubmitField('Search')


class AddNewMovieForm(Form):
    """
    通过豆瓣电影id添加到本地数据库
    """
    id = StringField('Id', validators=[DataRequired(), Length(min=5)])
    submit = SubmitField('Add')