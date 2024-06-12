import re
from . import main
from flask import redirect


#Обрабочтик ошибок
@main.errorhandler(Exception)
def error_page(e):
    """
    Handle errors
    :param e: error that occurred in the system
    :return: redirect to a different page
    """
    if re.search("404", str(e)):
        return redirect('/')
    else:
        print(e)
        return 'OOPS! Something went wrong'

