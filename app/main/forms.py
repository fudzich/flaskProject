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
    submit = SubmitField('Send')

class ThreadForm(FlaskForm):
    name = StringField('Name: ', validators=[DataRequired()])
    submit = SubmitField('Create Thread')

class ChangeRoleForm(FlaskForm):
    role = SelectField('Role: ', choices=[(1, 'Admin'), (2, 'User'), (3, 'Moderator')],
                         validators=[DataRequired()])
    submit = SubmitField('Change Role')
