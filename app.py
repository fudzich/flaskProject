from flask import Flask

import os
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/flaskproject_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['Mail_SERVER'] = 'smtp.googlemail.com'
app.config['Mail_PORT'] = 587
app.config['Mail_USERNAME'] = "alextesttestovik@gmail.com"
app.config['MAIL_PASSWORD'] = "jhkq wdsa hbei uyil"
app.config['Mail_USE_TLS'] = True
app.config['Mail_USE_SSL'] = False

db = SQLAlchemy(app)
mail = Mail(app)

class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return '<Test %r>' % self.name


class Gender(db.Model):
    __tablename__ = 'genders'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship('User', backref='gender')
    def __repr__(self):
        return '<Gender %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, index=True)
    password = db.Column(db.String(50))
    gender_id = db.Column(db.Integer, db.ForeignKey('genders.id'))

    def __repr__(self):
        return '<User %r>' % self.username


if __name__ == '__main__':
    app.run()

import routes