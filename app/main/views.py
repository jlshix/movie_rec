# coding: utf-8
# Created by leo on 17-4-8.
"""
main 蓝本的视图
"""
from . import main
from flask import render_template, flash, request, session, redirect, url_for
from forms import SearchForm, AddNewMovieForm, RatingForm
from app import mg, db, recommender
from utils import add_douban_movie, paginate
from app.models import User, Wt, Like, Rating
from flask_login import login_required, current_user
from utils import rec_sum


@main.route('/', methods=['GET', 'POST'])
def index():
    """
    主页 跳转至搜索
    :return: redirect
    """
    return redirect(url_for('.search'))


@main.route('/user/<id>', methods=['GET', 'POST'])
@login_required
def user(id):
    """
    用户页面 待完善
    :param id:
    :return:
    """
    user = User.objects(id=id).first()
    wts = Wt.objects(user=user).order_by('type')
    likes = Like.objects(user=user)
    ratings = Rating.objects(uid=user.uid)
    return render_template('user.html', user=user, wts=wts, likes=likes, ratings=ratings)


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
        movies = mg.db.movie.find({'title': {'$regex': name}})
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
            insert_id = mg.db.movie.insert_one(movie)
            if insert_id:
                flash(movie['title']+' added, thanks for your contribution!')
                return render_template('add-new-movie.html', form=form)
        else:
            flash('did not find movie with your input id')
            return render_template('add-new-movie.html', form=form)
    return render_template('add-new-movie.html', form=form)


@main.route('/subject/<id>', methods=['GET', 'POST'])
def movie_subject(id):
    movie = mg.db.movie.find_one({'_id': id})
    return render_template('movie.html', movie=movie)


@main.route('/subject/<id>/rating', methods=['GET', 'POST'])
@login_required
def movie_rating(id):
    form = RatingForm()
    movie = mg.db.movie.find_one({'_id': id})
    form.uid.data = current_user.uid
    form.mid.data = movie['lens_id']
    form.name.data = movie['title']
    if form.validate_on_submit() and request.method == 'POST':
        Rating(
            uid=int(form.uid.data),
            mid=int(form.mid.data),
            name=form.name.data,
            rating=float(form.rating.data),
            title=form.title.data,
            content=form.content.data
        ).save()
        recommender.add_ratings([[
            int(form.uid.data), int(form.mid.data), float(form.rating.data)
        ]])
        flash('rating recorded, retraining model...')
        return redirect(url_for('main.movie_rating', id=id))
    return render_template('rating.html', movie=movie, form=form)


@main.route('/lens2mid/<id>', methods=['GET', 'POST'])
def lens2mid(id):
    movie = mg.db.movie.find_one({'lens_id': int(id)})
    return redirect(url_for('main.movie_subject', id=movie['_id']))