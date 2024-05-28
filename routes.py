import re

from app import app, User, Gender, mail
from flask import request, redirect, render_template, abort, session
from flask import make_response
import random
from forms import LoginForm, MailForm
from flask_mail import Message

flag = True

un = 'username'
p = 'password'
g = 'gender'

@app.before_request
def before_request():
    global flag
    path = request.path
    browser = request.user_agent
    if re.search("Chrome", str(browser)) and flag:
        flag = False
        response = make_response(redirect(path))
        response.set_cookie('flag', str(random.randrange(1000)))
        return response

@app.route('/')
def hello_world():
    return render_template('mainPage.html')

@app.route('/index')
def index():
    user = {"username": "Alex"}
    return render_template('index.html', user = user)

@app.route('/rp/<name>')
def rp(name):
    #return "This is a random page made for {}!".format(name)
    return render_template('person.html', name = name)

# @app.errorhandler(Exception)
# def error_page(e):
#     if re.search("404", str(e)):
#         return redirect('/')
#     else:
#         print(e)
#         return 'OOPS! Something went wrong'

@app.route('/test_e')
def error_test():
    abort(500)
    return "somethin somethin"

@app.route('/form', methods=['GET', 'POST'])
def test_form():
    global un, p, g
    form = LoginForm()
    if form.validate_on_submit():
        # session['username'] = form.username.data
        # session['password'] = form.password.data
        # session['gender'] = form.gender.data
        user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
        if user is not None:
            un = user.username
            p = user.password
            g = Gender.query.get(user.gender_id).name
            return redirect('/profile')
        else:
            return redirect('/form')
    return render_template('formTemplate.html', form=form)

@app.route('/profile')
def profile_page():
    username = un
    password = p
    gender = g
    print(username, password, gender)
    if username is None:
        return render_template('profile.html')
    else:
        return render_template('profile.html',
                               username=username, password=password, gender=gender)

@app.route('/mail', methods=['GET', 'POST'])
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