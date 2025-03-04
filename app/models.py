from flask_login import UserMixin
from .exts import db
from werkzeug.security import generate_password_hash, check_password_hash
from .exts import login_manager


#Тестовая ДБ
class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return '<Test %r>' % self.name


#Дб с ролями пользователей
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    slug = db.Column(db.String(50), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return self.name


#ДБ с полами пользователей
class Gender(db.Model):
    __tablename__ = 'genders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship('User', backref='gender')

    def __repr__(self):
        return self.name


#ДБ с пользователями
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, index=True)
    password = db.Column(db.String(128))
    gender_id = db.Column(db.Integer, db.ForeignKey('genders.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    senders = db.relationship('Post', backref='user')

    @property
    def password_read(self):
        raise AttributeError('You cannot read the password attribute')

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def has_role(self, role_id):
        return Role.query.get(role_id) == self.role_id

    def __repr__(self):
        return '<User %r>' % self.username


class Thread(db.Model):
    __tablename__ = 'threads'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    posts = db.relationship('Post', backref='thread')

    def __repr__(self):
        return '<Thread %r>' % self.name


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    input = db.Column(db.String(500))
    thread_id = db.Column(db.Integer, db.ForeignKey('threads.id'))

    def __repr__(self):
        return self.input


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
