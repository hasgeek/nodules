# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, TextField

class DeleteForm(Form):
    # just the csrf info
    pass


# FIX THIS: get the jinja TemplateLoader here and check if the template exists.
def template_exists(form, field):
    return True


class TemplateMixin(Form):
    template = TextField(validators=[template_exists])


class ThemeMixin(Form):
    theme = TextField()
