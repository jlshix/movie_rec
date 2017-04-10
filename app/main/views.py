# coding: utf-8
# Created by leo on 17-4-8.
"""
main 蓝本的视图
"""
from . import main
from flask import render_template, flash, request, session, redirect, url_for
from forms import SearchForm, AddNewMovieForm
from app import mg
from utils import add_douban_movie, paginate


@main.route('/', methods=['GET', 'POST'])
def index():
    """
    主页 待完善
    :return: render
    """
    form = SearchForm()
    if form.validate_on_submit():
        name = form.name.data
        movies = mg.db.spider.find({'title': {'$regex': name}})
        # movies = mg.db.spider.find({'$or': [{'_id': id}, {'title': {'$regex': name}}]}).limit(10)

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


@main.route('/search/', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        name = form.name.data
        return redirect(url_for('.search', s=name, page=1))

    if 'page' not in request.args and 's' not in request.args:
        return render_template('search.html', form=form)
    else:
        name = request.args['s']
        page = request.args['page']
        movies = mg.db.spider.find({'title': {'$regex': name}})
        pagination = paginate(movies, int(page), 12, False)
        form.name.data = name
        return render_template('search-list.html', form=form, pagination=pagination)


@main.route('/add', methods=['GET', 'POST'])
def add_new_movie():
    form = AddNewMovieForm()
    if form.validate_on_submit():
        id = form.id.data
        if not id.strip():
            flash('something wrong with your input id')
            return render_template('add-new-movie.html', form=form)
        movie = add_douban_movie(id)
        if movie:
            insert_id = mg.db.spider.insert_one(movie)
            if insert_id:
                flash(movie['title']+' added, thanks for your contribution!')
                return render_template('add-new-movie.html', form=form)
        else:
            flash('did not find movie with your input id')
            return render_template('add-new-movie.html', form=form)
    return render_template('add-new-movie.html', form=form)


@main.route('/subject/<id>')
def movie_subject(id):
    return id