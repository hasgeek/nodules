# -*- coding: utf-8 -*-

from wtforms import TextField, ValidationError
from wtforms.validators import Required
from .models import Folder
from baseframe.forms import Form


def valid_folder_name(form, field):
    fname = field.data
    f = Folder.query.filter_by(name=fname).first()
    if f:
        raise ValidationError("Folder already exists at this url. Please choose a different URL name.")


class NewFolderForm(Form):
    name = TextField('URL name', validators=[Required(), valid_folder_name])
    title = TextField('Title', validators=[Required()])
