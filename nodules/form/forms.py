# -*- coding: utf-8 -*-

from flask.ext.wtf import (Form, TextField, TextAreaField, FormField,
                    Required, SelectField, FieldList, ListWidget,
                    SubmitField)


__all__ = ['MetaForm']


wtform_field_types = ('BooleanField', 'DecimalField', 'DateField', 'DateTimeField',
    'FloatField', 'IntegerField', 'RadioField', 'SelectField',
    'SelectMultipleField', 'StringField')

all_field_types = [(f, f.replace('Field', '')) for f in wtform_field_types]


class Question(Form):
    """
    Each field of the form
    """
    label = TextField(validators=[Required()])
    description = TextField()
    type = SelectField(choices=all_field_types)
    choices = FieldList(TextField()) # choices for SelectField, RadioField, BooleanField


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
