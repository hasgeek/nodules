# -*- coding: utf-8 -*-

from __future__ import absolute_import

from ._version import *

# Import basic nodes like User

from nodules.models import *

# Do not import content nodes until they are required by the client app


# initialize app
def init_app(app):
    load_templates(app)

def load_templates(app):
    import jinja2, os.path
    this_dir = os.path.abspath(os.path.dirname(__file__))
    loader = jinja2.ChoiceLoader([
                app.jinja_loader,
                jinja2.FileSystemLoader([os.path.join(this_dir, 'templates')])
            ])
    app.jinja_loader = loader
