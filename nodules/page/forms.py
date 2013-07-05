# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, TextField, TextAreaField, Required

from nodules.models import RichText
from nodules.forms import TemplateMixin


class RichTextField(TextAreaField):
    def populate_obj(self, obj, name):
        rt = RichText(self.data)
        setattr(obj, name, rt)


class PageForm(TemplateMixin, Form):
    title = TextField('title', validators=[Required()])
    description = RichTextField('description')

    def populate_obj(self, obj):
        super(Form, self).populate_obj(obj)
        obj.make_name()
        obj.properties['template'] = self.template.data
