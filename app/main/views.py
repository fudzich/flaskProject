import re
import random
from flask import request, redirect, render_template, abort, make_response
from flask_mail import Message
from flask_login import login_required, current_user
from app.main.forms import MailForm, MessageForm, ThreadForm
from .. import mail
from . import main
from ..models import Post, User, Thread, Role
from .. import db
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
    Renders the home page with all threads
    :return: main page
    """
    threads = Thread.query.all()
    form = ThreadForm()

    if form.validate_on_submit():
        thread = Thread(name=form.name.data)
        db.session.add(thread)
        db.session.commit()
        return redirect("/")
    return render_template('mainPage.html', list=list, threads = threads, form=form)

@main.route('/thread/<thread_name>', methods=['GET', 'POST'])
def thread_page(thread_name):
    """
    Renders the page with posts
    :return: thread page
    """
    exists = Thread.query.filter_by(name=thread_name).first() is not None
    posts = Post.query.all()
    users = User.query.all()
    roles = Role.query.all()
    form = MessageForm()

    if exists:
        thread_id = Thread.query.filter_by(name=thread_name).first().id

        if form.validate_on_submit():
            post = Post(sender_id = current_user.id, input = form.body.data, thread_id = thread_id)
            db.session.add(post)
            db.session.commit()
            return redirect("/thread/" + thread_name)

        return render_template('thread.html', list=list, posts=posts, users=users,
                                    form = form, thread_name = thread_name, thread_id = thread_id, roles = roles)
    else:
        return render_template('noThread.html')


@main.route('/thread/<thread_name>/delete/<post_id>', methods=['GET', 'POST'])
def delete_post_page(thread_name,post_id):
    print()
    if current_user.is_authenticated:
        exists = Post.query.filter_by(id=post_id).first() is not None
        if exists:

            sender_id = Post.query.filter_by(id=post_id).first().sender_id
            role_id = User.query.filter_by(id=sender_id).first().role_id

            print(current_user.role_id)

            if (current_user.role_id == 1 or (current_user.role_id == 3 and role_id != 1)
                    or current_user.role_id == sender_id):
                db.session.query(Post).filter(Post.id == post_id).delete()
                db.session.commit()
                return redirect("/thread/" + thread_name)


    return render_template('notAuth.html')



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
    if current_user.is_authenticated:
        if current_user.role_id == 1 or current_user.role_id == 3:
            form = MailForm()
            if form.validate_on_submit():
                recipient = form.mail.data
                template = form.body.data
                send_mail(recipient, 'Forum Website', template)
                return redirect('/')
            return render_template('mailForm.html', form=form)

    return render_template('notAuth.html')


def send_mail(to, subject, template):
    msg = Message(subject,
                  sender="app.config['MAIL_USERNAME']",
                  recipients=[to])
    msg.body = template
    mail.send(msg)
