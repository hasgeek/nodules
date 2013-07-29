# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, TextField, Required
import utils


class EmptyForm(Form):
    # just the csrf info
    pass


# FIX THIS: get the jinja TemplateLoader here and check if the template exists.
def template_exists(form, field):
    return True


class TemplateFieldMixin(object):
    template = TextField(validators=[template_exists])


class ThemeFieldMixin(Form):
    theme = TextField('Theme')


class TagsField(TextField):
    def populate_obj(self, obj, name):
        #@@ TODO - make get_or_make_tags so that a single round trip to the DB to do this
        tags = [utils.get_or_make_tag(t.strip()) for t in self.data.strip().split(',')]
        setattr(obj, name, tags)

    def process_data(self, value):
        if value:
            self.data = ','.join([t.name for t in value])
        else:
            self.data = ''


class TagsFieldMixin(object):
    tags = TagsField()


class EditTagForm(Form):
    title = TextField('Title', validators=[Required()])
