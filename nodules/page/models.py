# -*- coding: utf-8 -*-

from flask import Markup
from markdown import markdown

from nodular import NodeMixin, Node, db
from nodules.models import User

class PageType(NodeMixin, Node):
    __tablename__ = u'page'
    title = db.Column(db.Unicode(250), nullable=False)
    user_id = db.Column(None, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User, backref=db.backref('pages',
            cascade='all, delete-orphan', lazy='dynamic'))
    _content = db.Column('content', db.UnicodeText, nullable=False, default=u'')
    _content_html = db.Column('content_html', db.UnicodeText, nullable=False, default=u'')
    content_format = db.Column(db.Unicode(250), nullable=False)    # html / markdown

    def permissions(self, user, inherited=None):
        perms = super(PageType, self).permissions(user, inherited)
        perms.add('view')  # Grant everyone view access
        if user == self.user:
            perms.add('edit')
            perms.add('delete')
        return perms

    @property
    def content(self):
       return self._content

    @content.setter
    def content(self, value):
        self._content = value
        if self.content_format != 'html':
            self._content_html = markdown(value)
        else:
            self._content_html = value

    @property
    def content_html(self):
       return Markup(self._content_html)
