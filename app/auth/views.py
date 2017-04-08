# coding: utf-8
# Created by leo on 17-4-8.
from hashlib import sha1
from flask import request, session, url_for, render_template, redirect, flash
from . import auth
from app import db
from ..models import User
from forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        pw = form.password.data
        user = User.query.filter_by(email=email).first()
        if user.password == pw:
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.index'))
        else:
            flash('wrong password')
            return redirect(url_for('.login'))
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data
        )
        try:
            db.session.add(user)
            db.session.commit()
            flash('Please Login')
            return redirect(url_for('.login'))
        except Exception, e:
            flash(e)
            return redirect(url_for('.register'))
    return render_template('auth/register.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('you have logged out')
    return redirect(url_for('main.index'))