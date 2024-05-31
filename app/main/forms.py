from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, EqualTo, Email


class LoginForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password: ',
                              validators=[DataRequired(), EqualTo('password')])
    # gender = SelectField('Gender: ',
    #                      choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
    #                      validators=[DataRequired()])
    submit = SubmitField('Login')


class MailForm(FlaskForm):
    mail = EmailField('Mail: ', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Email')
