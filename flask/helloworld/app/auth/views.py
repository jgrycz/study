from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, \
    ResetPasswordForm, SetNewPasswordForm, ChangeEmailForm
from .. import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Incorrect username or password')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You were log out")
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        url = url_for('auth.confirm', token=token, _external=True)
        flash('Before you log in activate your account please, clicking following url: {}'.format(url))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('Your account has been confirmed')
    else:
        flash('Confirmation email is incorrect or has expired')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('confirm')
@login_required
def resend_information():
    token = current_user.generate_confirmation_token()
    url = url_for('auth.confirm', token=token, _external=True)
    flash('Before you log in activate your account please, clicking following url: {}'.format(url))
    return redirect(url_for('main.index'))



@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=current_user.email).first()
        if user.verify_password(form.old_password.data):
            user.password = form.new_password.data
            db.session.add(user)
            db.session.commit()
            flash('Your password has been changed!')
        else:
            flash('Incorrect current password')
    return render_template('auth/change_password.html', form=form)


@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            url = url_for('auth.set_new_password', token=token, _external=True)
            flash('To reset your password go to following url: {}'.format(url))
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password_request.html', form=form)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = SetNewPasswordForm()
    if form.validate_on_submit():
        User.reset_password(token, form.new_password.data)
        db.session.commit()
        flash('Your password has been changed!')
        return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change_email_request', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=current_user.email).first()
        token = user.generate_change_email_token(form.new_email.data)
        url = url_for('auth.confirm_change_email', token=token, _external=True)
        flash('To confirm your email change visit following url: {}'.format(url))
        return redirect(url_for('main.index'))
    return render_template('auth/change_email_request.html', form=form)


@auth.route('/confirm_change_email/<token>', methods=['GET', 'POST'])
@login_required
def confirm_change_email(token):
    if User.change_email(token):
        db.session.commit()
        flash('Your email address has been changed!')
    else:
        flash('Change email url is incorrect or has expired')
    return redirect(url_for('main.index'))
