# -*- coding: utf-8 -*-

from nodular import NodeMixin
from nodules import Node, db
from nodules.models import User, RichTextColumn, RichText

__all__ = ['Page']

class Page(NodeMixin, Node):
    __tablename__ = u'page'

    description = RichTextColumn(db, 'description')
    # auto save the page for every 1 minute. Disable autosave by setting it to 0.
    autosave = 60000

    def __init__(self, *args, **kwargs):
        kwargs['description'] = RichText(kwargs.get('description', ''))
        super(Page, self).__init__(*args, **kwargs)

    def permissions(self, user, inherited=None):
        perms = super(Page, self).permissions(user, inherited)
        perms.add('view')  # Grant everyone view access
        if user == self.user:
            perms.add('edit')
            perms.add('publish')    # publish/unpublish
            perms.add('delete')
        return perms

    def __repr__(self):
        return "Page <%s>" % self.title
