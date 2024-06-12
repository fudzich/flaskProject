from flask import Flask
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from app.exts import *
from app.models import *
from config import config


#Вью ограничивающий доступ к панеле админа
class AdminView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated:
            return current_user.role_id == 1
        return False


login_manager.login_view = 'auth.login'
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(Role, db.session))
admin.add_view(AdminView(Gender, db.session))


def register_extensions(app):
    db.init_app(app)
    admin.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    register_extensions(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    return app
