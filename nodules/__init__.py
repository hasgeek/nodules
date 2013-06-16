# -*- coding: utf-8 -*-

from __future__ import absolute_import

from ._version import *

from nodular import NodeRegistry, Node

# Import basic nodes like User

from nodules.models import User, db

# Do not import content nodes until they are required by the client app

# the following imports should be configurable
from nodules import page

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

def load_templates(app):
    import jinja2, os.path
    this_dir = os.path.abspath(os.path.dirname(__file__))
    loader = jinja2.ChoiceLoader([
                app.jinja_loader,
                jinja2.FileSystemLoader([os.path.join(this_dir, 'templates')])
            ])
    app.jinja_loader = loader
