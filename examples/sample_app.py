# -*- coding: utf-8 -*-

import os, jinja2, importlib, warnings
from flask import Flask, render_template, request, flash, redirect

from baseframe import baseframe, assets
import coaster.app
from nodular import Node
import nodules
from nodules import db, registry
from nodules.page import Page


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'fasfdaf'

app.config['NODULES'] = ('PAGE', 'FOLDER', )
app.config['PAGE_TEMPLATE_THEME'] = 'templates/mytheme/'
# app.config['PAGE_BASEURL'] = '/pages'   # if this is not set, publish `page` nodule at '/

registry.register_node(Node)
from nodules.folder import Folder   # import this to make the root node as folder

 # fix this
def get_root():
    root = Folder.query.filter_by(title='root').first()
    if not root:
        root = Folder(title=u'root')
        root.make_name()
        db.session.add(root)
        db.session.commit()
    return root


# initialize nodules
def init_nodules(app):
    """Load the templates, set root node and initialize the required nodules"""
    load_templates(app)
    app.root = get_root()

    # the `init` of respective nodules
    for n in app.config.get('NODULES', []):
        n = n.lower()
        try:
            nodule = importlib.import_module('nodules.%s' % n)
        except Exception, e:
            warnings.warn(e.message)
        else:
            nodule_base_path = app.config.get('%s_BASEURL' % n.upper(), '/')
            nodule_publisher = nodule.init_nodule(app.root, registry, nodule_base_path)
            setattr(app, '%s_pub' % n, nodule_publisher)


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
    template_dirs = get_theme_dirs(app)
    nodules_dir = os.path.abspath(os.path.dirname(nodules.__file__))
    template_dirs.append(os.path.join(nodules_dir, 'templates'))
    loader = jinja2.ChoiceLoader([
                app.jinja_loader, jinja2.FileSystemLoader(template_dirs)
            ])
    app.jinja_loader = loader


def error404(error):
    return 'page not found', 404


def init_for(env):
    coaster.app.init_app(app, env)
    baseframe.init_app(app, requires=['baseframe'])
    app.error_handlers[404] =  error404
    db.init_app(app)
    db.app = app
    db.create_all()
    init_nodules(app)


@app.route('/', defaults={'anypath': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:anypath>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def publish_path(anypath):
    return app.folder_pub.publish(anypath)


if __name__ == '__main__':
    init_for('dev')
    app.run(port=4500, debug=True)
