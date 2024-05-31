import re
from . import main
from flask import redirect


@main.errorhandler(Exception)
def error_page(e):
    if re.search("404", str(e)):
        return redirect('/')
    else:
        print(e)
        return 'OOPS! Something went wrong'

