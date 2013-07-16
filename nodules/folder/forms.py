# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, TextField, Required

# @@TODO
def existing_folder(form, field):
    pass


class NewFolderForm(Form):
    name = TextField('URL name', validators=[Required()])
    title = TextField('Title', validators=[Required()])
