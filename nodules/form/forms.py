# -*- coding: utf-8 -*-

import wtforms
from wtforms import (TextField, TextAreaField, FormField,
                    SelectField, FieldList, SubmitField)
from wtforms.validators import Required
from wtforms.widgets import ListWidget
from baseframe.forms import Form

__all__ = ['MetaForm']


wtform_field_types = ('BooleanField', 'DateField', 'DateTimeField',
    'FloatField', 'IntegerField', 'RadioField', 'SelectField',
    'SelectMultipleField', 'StringField')

all_field_types = [(f, f.replace('Field', '')) for f in wtform_field_types]
all_field_types.insert(0, ("", "--Select--"))


# Subclassed from wtforms.Form instead of flask.wtf.Form to avoid mutliple csrf fields in MetaForm
class Question(wtforms.Form):
    """
    Each question field of the MetaForm.
    """
    label = TextField(validators=[Required()])
    description = TextField()
    type = SelectField(choices=all_field_types, validators=[Required()])
    choices = FieldList(TextField(validators=[Required()])) # choices for select, radio

    def validate(self):
        if self.type in ('SelectField', 'SelectMultipleField', 'RadioField'):
            self.choices.min_entries = 2
        rv = wtforms.Form.validate(self)
        return bool(rv)


class MetaForm(Form):
    """
    Form to create forms
    """
    title = TextField(validators=[Required()])
    description = TextAreaField()
    questions = FieldList(FormField(Question), min_entries=2)

    def populate_obj(self, obj):
        # FieldList populate_obj expects to fill in multiple question objects,
        # which is not the case. so, override that
        for name, field in self._fields.iteritems():
            if name != 'questions':
                field.populate_obj(obj, name)
            else:
                obj.questions = self.questions.data # a list of dicts
