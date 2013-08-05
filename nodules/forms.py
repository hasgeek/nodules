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
    def process_data(self, value):
        # list of tag objects to csv
        if value:
            self.data = ','.join([t.name for t in value])
        else:
            self.data = ''

    def process_formdata(self, data):
        # csv to list of tag objects
        if data[0]:
            tag_titles = (t.strip() for t in data[0].strip(' ,').split(','))
            self.data = utils.get_or_make_tags(tag_titles)
        else:
            self.data = []


class TagsFieldMixin(object):
    tags = TagsField()


class EditTagForm(Form):
    title = TextField('Title', validators=[Required()])
