# ~*~ coding:utf-8 ~*~

""" 
    Main wiki functions are defined here. 

    naming convention: 
        function+class names are in camelCase format
        variable names, class+instance methods are in under_scores
"""

from djtemps import render_to_response
from .auth import *
from .user import *
from .wiki import *

def index(request):
    return render_to_response("index.jinja", locals())
