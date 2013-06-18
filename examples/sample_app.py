# -*- coding: utf-8 -*-

from flask import Flask

from baseframe import baseframe, assets
import coaster.app
import nodules
from nodules import registry, db
from nodules.page import Page, PageView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'fasfdaf'
app.config['PAGE_TEMPLATE_THEME'] = 'templates/my_theme/'


def error404(error):
    return 'page not found', 404


def init_for(env):
    coaster.app.init_app(app, env)
    baseframe.init_app(app, requires=['baseframe'])
    app.error_handlers[404] =  error404
    db.init_app(app)
    db.app = app
    db.create_all()
    nodules.init_app(app)


@app.route('/<path:anypath>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def publish_path(anypath):
    return app.pagepub.publish(anypath)


if __name__ == '__main__':
    init_for('dev')
    app.run(port=4500, debug=True)
