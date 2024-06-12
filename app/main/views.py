import re
import random
from flask import request, redirect, render_template, abort, make_response
from flask_mail import Message
from flask_login import login_required, current_user
from app.main.forms import MailForm
from .. import mail
from . import main
from ..decorators import admin_required


flag = True


#Создание куки до загрузки страницы
@main.before_request
def before_request():
    global flag
    path = request.path
    browser = request.user_agent
    if re.search("Chrome", str(browser)) and flag:
        flag = False
        response = make_response(redirect(path))
        response.set_cookie('flag', str(random.randrange(1000)))
        return response


#Главная страница вебсайта
@main.route('/', methods=['GET', 'POST'])
def hello_world():
    """
    Renders the home page
    :return: main page
    """
    return render_template('mainPage.html', list=list)


#Страница создающая текст на основе ссылки
@main.route('/rp/<name>')
def rp(name):
    """
    Takes a name parameter and returns HTML response with a greeting message
    :param name: The inputted name
    :return: HTML response
    """
    return render_template('person.html', name = name)


#Страница для тестирования выдающаяя ошибку
@main.route('/test_e')
def error_test():
    abort(500)


#Страница с профилем аккаунта
@main.route('/profile')
@login_required
def profile_page():
    """
    Renders the profile page of the user
    :return: profile page
    """
    user = current_user
    if user.username is None:
        return render_template('profile.html')
    else:
        return render_template('profile.html',
                               username=user.username, role=user.role, gender=user.gender)


#Страница отправляющая письмо на почту
@main.route('/mail', methods=['GET', 'POST'])
def mail_page():
    """
    Renders the Mail page of the user that allows to send emails
    :return: Mail page
    """
    form = MailForm()
    if form.validate_on_submit():
        recipient = form.mail.data
        template = form.body.data
        send_mail(recipient, 'Test email', template)
        return redirect('/')
    return render_template('mailForm.html', form=form)


def send_mail(to, subject, template):
    msg = Message(subject,
                  sender="app.config['MAIL_USERNAME']",
                  recipients=[to])
    msg.body = template
    mail.send(msg)
