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
from app.models import User, Wt, Like, Rating
from flask_login import login_required


@main.route('/', methods=['GET', 'POST'])
def index():
    """
    主页 待完善
    :return: render
    """
    return redirect(url_for('.search'))


@main.route('/user/<id>', methods=['GET', 'POST'])
@login_required
def user(id):
    """
    用户页面 待完善
    :param name:
    :return:
    """
    user = User.objects(id=id).first()
    wts = Wt.objects(user=user).order_by('type')
    likes = Like.objects(user=user)
    return render_template('user.html', user=user, wts=wts, likes=likes)


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
    movie = mg.db.spider.find({'_id': id}).limit(1)
    return render_template('movie.html', movie=movie[0])
