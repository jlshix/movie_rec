# coding: utf-8
# Created by leo on 17-4-8.

from flask import (request, session, url_for,
                   render_template, redirect, flash)
from . import auth
from app import db
from ..models import User
from forms import LoginForm, RegisterForm
from flask_login import login_user, logout_user, login_required, current_user
from app.utils import send_email


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user.verify_password(password):
            login_user(user, form.remember_me.data)
            if request.args['next']:
                return redirect(request.args['next'])
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
            token = user.generate_confirmation_token()
            send_email(form.email.data, 'Confirm Your Account',
                       'auth/email/confirm', user=user, token=token)
            flash('Please check your mailbox to verify your account')
            db.session.commit()
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


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        flash('Your account have been confirmed before')
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('Thanks to confirm your account')
    else:
        flash('This confirmation link is invalid or has expired')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def reconfirm():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('New confirmation email has been sent')
    return redirect(url_for('main.index'))
