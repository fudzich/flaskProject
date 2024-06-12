from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_mail import Mail
from flask_login import LoginManager


db = SQLAlchemy()
admin = Admin()
login_manager = LoginManager()
mail = Mail()

#Существует для обхода кругового импорта
