from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, EqualTo, Email, Length

from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired(), Length(min=1, max=50)])
    password = PasswordField('Password: ', validators=[DataRequired(), Length(min=1, max=50)])
    password2 = PasswordField('Confirm Password: ',
                              validators=[DataRequired(), EqualTo('password', message='Passwords must match'),
                                          Length(min=1, max=50)])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password: ',
                              validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    gender = SelectField('Gender: ', choices=[(4, 'Male'), (5, 'Female'), (6, 'Other')],
                         validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Please use a different username.')
