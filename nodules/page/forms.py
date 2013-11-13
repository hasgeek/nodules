# -*- coding: utf-8 -*-

from wtforms import TextField, TextAreaField
from wtforms.validators import Required
from baseframe.forms import Form

from nodules.models import RichText
from nodules.forms import TemplateFieldMixin, TagsFieldMixin


class RichTextField(TextAreaField):
    def populate_obj(self, obj, name):
        rt = RichText(self.data)
        setattr(obj, name, rt)


class PageForm(TagsFieldMixin, TemplateFieldMixin, Form):
    title = TextField('title', validators=[Required()])
    description = RichTextField('description')

    def populate_obj(self, obj):
        super(Form, self).populate_obj(obj)
        obj.make_name()
        obj.properties['template'] = self.template.data
