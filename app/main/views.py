import re
import random
from flask import request, redirect, render_template, abort, make_response
from flask_mail import Message
from flask_login import login_required, current_user
from app.models import User, Gender
from app.main.forms import MailForm
from .. import mail
from . import main


flag = True

# un = 'username'
# p = 'password'
# g = 'gender'


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


@main.route('/')
def hello_world():
    return render_template('mainPage.html')


@main.route('/index')
def index():
    user = {"username": "Alex"}
    return render_template('index.html', user = user)


@main.route('/rp/<name>')
def rp(name):
    #return "This is a random page made for {}!".format(name)
    return render_template('person.html', name = name)


@main.route('/test_e')
def error_test():
    abort(500)
#    return "something-something"


# @main.route('/form', methods=['GET', 'POST'])
# def test_form():
#     global un, p, g
#     form = LoginForm()
#     if form.validate_on_submit():
#         # session['username'] = form.username.data
#         # session['password'] = form.password.data
#         # session['gender'] = form.gender.data
#         user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
#         if user is not None:
#             un = user.username
#             p = user.password
#             g = Gender.query.get(user.gender_id).name
#             return redirect('/profile')
#         else:
#             return redirect('/form')
#     return render_template('formTemplate.html', form=form)


@main.route('/profile')
@login_required
def profile_page():
    user = current_user
    print("in profile:" + user.username, user.gender)
    if user.username is None:
        return render_template('profile.html')
    else:
        return render_template('profile.html',
                               username=user.username, password=user.password, gender=user.gender)


@main.route('/mail', methods=['GET', 'POST'])
def mail_page():
    form = MailForm()
    if form.validate_on_submit():
        recipient = form.mail.data
        send_mail(recipient, 'Test email', 'test_mail')
        return redirect('/')
    return render_template('mailForm.html', form=form)


def send_mail(to, subject, template):
    msg = Message(subject,
                  sender="app.config['MAIL_USERNAME']",
                  recipients=[to])
    msg.body = render_template(template + '.txt')
    mail.send(msg)


@main.route('/locked')
@login_required
def locked_page():
    return "Classified Info! For Authorised Only!"
