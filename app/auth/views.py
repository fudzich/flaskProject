from flask import redirect, render_template, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import User, Gender


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect('/profile')
        else:
            return redirect(url_for('auth.login'))
    return render_template('formTemplate.html', form=form)


@auth.route('/reg', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
#                    password=form.password.data,
                    gender=Gender.query.get(form.gender.data))
        db.session.add(user)
        user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('regTemplate.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.hello_world'))
