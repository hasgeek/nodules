# -*- coding: utf-8 -*-

from __future__ import absolute_import

from ._version import *

import os.path, jinja2

from nodular import NodeRegistry, Node

# Import basic nodes like User

from nodules.models import User, db

# Do not import content nodes until they are required by the client app

# the following imports should be configurable
from nodules import page

__all__ = ['page', 'registry' 'User', 'db', '__version__', '__version_info__']

registry = NodeRegistry()
registry.register_node(Node)

# fix this
def get_root():
    root = Node.query.filter_by(name='index').first()
    if not root:
        root = Node(name=u'index', title=u'Index Node')
        db.session.add(root)
        db.session.commit()
    return root

# initialize app
def init_app(app):
    load_templates(app)
    app.root_node = get_root()
    # the `init_app` of respective nodules - should be configurable
    page.init_app(app)


def get_theme_dirs(app):
    paths = [v for (k, v) in app.config.iteritems()
                if k.upper().endswith('TEMPLATE_THEME')]
    return [os.path.abspath(p) for p in paths if os.path.exists(p)]


def load_templates(app):
    """
    Look for the templates in the following places, in that order -
    1. app's template directory, by default <app_dir>/templates/
    2. theme directories in app.config e.g.PAGE_THEME_DIR # relative to <app_dir>
    3. nodules/templates/
    """
    this_dir = os.path.abspath(os.path.dirname(__file__))
    template_dirs = get_theme_dirs(app)
    template_dirs.append(os.path.join(this_dir, 'templates'))
    loader = jinja2.ChoiceLoader([
                app.jinja_loader, jinja2.FileSystemLoader(template_dirs)
            ])
    app.jinja_loader = loader
