from . import db


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