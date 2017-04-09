# coding: utf-8
# Created by leo on 17-4-8.
"""
main 蓝本的视图
"""
from . import main
from flask import render_template, flash
from forms import SearchForm, AddNewMovieForm
from app import mg
from utils import add_douban_movie


@main.route('/', methods=['GET', 'POST'])
def index():
    """
    主页 待完善
    :return: render
    """
    form = SearchForm()
    if form.validate_on_submit():
        id = form.id.data
        name = form.name.data
        movies = mg.db.spider.find({'$or': [{'_id': id}, {'title': {'$regex': name}}]}).limit(10)

        return render_template('index.html', form=form, movies=movies)
    return render_template('index.html', form=form)


@main.route('/user/<int:id>', methods=['GET', 'POST'])
def user(id):
    """
    用户页面 待完善
    :param name:
    :return:
    """
    return 'Hello {}'.format(id)


@main.route('/add', methods=['GET', 'POST'])
def add_new_movie():
    form = AddNewMovieForm()
    if form.validate_on_submit():
        id = form.id.data
        movie = add_douban_movie(id)
        if movie:
            insert_id = mg.db.spider.insert_one(movie)
            if insert_id:
                flash(movie['title']+' added, thanks for your contribution!')
                return render_template('add-new-movie.html', form=form)
    return render_template('add-new-movie.html', form=form)