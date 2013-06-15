# -*- coding: utf-8 -*-

from nodular import NodeMixin, Node, db
from nodules.models import User, RichTextColumn

__all__ = ['PageType']

class PageType(NodeMixin, Node):
    __tablename__ = u'page'
    title = db.Column(db.Unicode(250), nullable=False)
    description = RichTextColumn(db, 'description')
    published_at = db.Column(db.DateTime) # None if not published

    def permissions(self, user, inherited=None):
        perms = super(PageType, self).permissions(user, inherited)
        perms.add('view')  # Grant everyone view access
        if user == self.user:
            perms.add('edit')
            perms.add('delete')
        return perms

    def __repr__(self):
        return "Page <%s>" % self.title
