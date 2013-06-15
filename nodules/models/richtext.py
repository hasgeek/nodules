# -*- coding: utf-8 -*-

from flask import Markup
from markdown import markdown

from nodules.models import db

__all__ = ['RichTextColumn', 'RichText']

class RichText(object):
    def __init__(self, text, format=None):
        self.text = text
        self.format = format or self.getformat()

        # store html only if the format is NOT HTML.
        if self.format == 'text':
            self.html = markdown(text)
        else:
            self.html = ''

    @classmethod
    def _from_db(cls, text, html, format):
        if text is not None:
            rt = RichText(text, format)
            rt.html = Markup(html or text)
            return rt
        else:
            return None

    def getformat(self):
        if self.text.startswith('<p>') and self.text.endswith('</p>'):
            return 'html'
        else:
            return 'text'

    def __composite_values__(self):
        return (self.text, self.html, self.format)

    def __str__(self):
        return self.text


def RichTextColumn(db, col_name):
    return db.composite(RichText._from_db,
             db.Column(col_name + '_text', db.UnicodeText),
             db.Column(col_name + '_html', db.UnicodeText),
             db.Column(col_name + '_format', db.Unicode(20)))
