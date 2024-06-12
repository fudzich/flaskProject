from flask import redirect, render_template, url_for
from flask_login import login_user, login_required, logout_user

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import User, Gender, Role
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import webbrowser


#Путь ко входу в аккаунт
@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login data processing
    :return: login form
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect('/profile')
        else:
            return redirect(url_for('auth.login'))
    return render_template('formTemplate.html', form=form)


#Путь к регистрации
@auth.route('/reg', methods=['GET', 'POST'])
def register():
    """
    Registration data processing
    :return: registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        webbrowser.open_new_tab(url_for('auth.google_auth'))
        if google_auth():
            user = User(username=form.username.data,
                        role=Role.query.get(2),
                        gender=Gender.query.get(form.gender.data))
            db.session.add(user)
            user.set_password(form.password.data)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            return render_template('regTemplate.html', form=form)
    return render_template('regTemplate.html', form=form)


#Путь к подтверждению аккаунта с помощью аакаунта гугл
@auth.route('/oauth')
def google_auth():
    """
    Google authorization
    :return: user verification
    """
    flow = (InstalledAppFlow.from_client_secrets_file(
        'client_secret.json',
        scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email',
                'https://www.googleapis.com/auth/userinfo.profile']))
    flow.run_local_server()
    credentials = flow.credentials
    user_info_service = build('oauth2', 'v2', credentials=credentials)
    user_info = user_info_service.userinfo().get().execute()

    return user_info['verified_email']


#Путь к выходу из аккаунта
@auth.route('/logout')
@login_required
def logout():
    """
    Logout user
    :return: main page
    """
    logout_user()
    return redirect(url_for('main.hello_world'))
