# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, TextField, TextAreaField, Required

from nodules.models import RichText


class RichTextField(TextAreaField):
    def populate_obj(self, obj, name):
        rt = RichText(self.data)
        setattr(obj, name, rt)


class PageForm(Form):
    title = TextField('title', validators=[Required()])
    description = RichTextField('description')
