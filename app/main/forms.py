from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, EqualTo, Email, Length


class MailForm(FlaskForm):
    mail = EmailField('Mail: ', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Email')
