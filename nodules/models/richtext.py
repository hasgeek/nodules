# -*- coding: utf-8 -*-

from markdown import markdown

from flask import Markup
from sqlalchemy.ext.mutable import MutableComposite

from nodules.models import db

__all__ = ['RichTextColumn', 'RichText']


class RichText(MutableComposite):
    def __init__(self, text, html=None, format=None):
        self.format = format or self.getformat(text)
        self.text = text

    def getformat(self, text):
        if text.startswith('<p>') and text.endswith('</p>'):
            return 'html'
        else:
            return 'text'

    def __setattr__(self, key, value):
        if key == 'text':
            if self.format == 'text':
                self._html = markdown(value)
            else:
                self._html = ''
        object.__setattr__(self, key, value)
        self.changed()

    def __composite_values__(self):
        return (self.text, self._html, self.format)

    def __str__(self):
        return self.text

    @property
    def html(self):
        return Markup(self._html or self.text)


def RichTextColumn(db, col_name):
    return db.composite(RichText,
             db.Column(col_name + '_text', db.UnicodeText),
             db.Column(col_name + '_html', db.UnicodeText),
             db.Column(col_name + '_format', db.Unicode(20)))
