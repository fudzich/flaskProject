from flask import redirect, render_template, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import User, Gender, Role

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import webbrowser

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
        webbrowser.open_new_tab(url_for('auth.google_auth'))
        if google_auth():
            user = User(username=form.username.data,
#                       password=form.password.data,
                        role=Role.query.get(2),
                        gender=Gender.query.get(form.gender.data))
            db.session.add(user)
            user.set_password(form.password.data)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            return render_template('regTemplate.html', form=form)
    print(form.errors)
    return render_template('regTemplate.html', form=form)


@auth.route('/oauth')
def google_auth():
    flow = (InstalledAppFlow.from_client_secrets_file(
        'client_secret.json',
        scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile']))
    flow.run_local_server()
    credentials = flow.credentials
    user_info_service = build('oauth2', 'v2', credentials=credentials)
    user_info = user_info_service.userinfo().get().execute()

    return user_info['verified_email']


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.hello_world'))
