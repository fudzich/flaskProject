from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, Email


#Форма для отправки почты
class MailForm(FlaskForm):
    mail = EmailField('Mail: ', validators=[DataRequired(), Email()])
    body = TextAreaField('Body: ', validators=[DataRequired()])
    submit = SubmitField('Send Email')


class MessageForm(FlaskForm):
    body = TextAreaField(validators=[DataRequired()])
    submit = SubmitField('Send Message')

class ThreadForm(FlaskForm):
    name = StringField('Name: ', validators=[DataRequired()])
    submit = SubmitField('Create Thread')
