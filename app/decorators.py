from functools import wraps
from flask import abort
from flask_login import current_user


def permission_required(permission):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.role_id == permission:
                return func(*args, **kwargs)
            return abort(403)
        return wrapper
    return decorator


def admin_required(f):
    return permission_required(1)(f)
