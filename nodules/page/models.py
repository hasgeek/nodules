# -*- coding: utf-8 -*-

from nodular import NodeMixin, Node, db
from nodules.models import User, RichTextColumn, RichText

__all__ = ['Page']

class Page(NodeMixin, Node):
    __tablename__ = u'page'

    title = db.Column(db.Unicode(250), nullable=False)
    description = RichTextColumn(db, 'description')
    published_at = db.Column(db.DateTime) # None if not published

    def __init__(self, *args, **kwargs):
        kwargs['description'] = RichText(kwargs.get('description', ''))
        super(Page, self).__init__(*args, **kwargs)

    def permissions(self, user, inherited=None):
        perms = super(Page, self).permissions(user, inherited)
        perms.add('view')  # Grant everyone view access
        if user == self.user:
            perms.add('edit')
            perms.add('delete')
        return perms

    def __repr__(self):
        return "Page <%s>" % self.title
