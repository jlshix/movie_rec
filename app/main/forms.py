# coding: utf-8
# Created by leo on 17-4-8.
"""
表格
"""

from flask_wtf import FlaskForm as Form
from wtforms import IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, AnyOf, NumberRange


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


class RatingForm(Form):
    """
    评分
    """
    uid = IntegerField('Uid', validators=[DataRequired()])
    mid = IntegerField('Mid', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=0, max=5)])
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')