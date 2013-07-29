# -*- coding: utf-8 -*-

from nodular import NodeMixin, Node, db

class Folder(NodeMixin, Node):
    __tablename__ = 'folder'

    def permissions(self, user, inherited=None):
        perms = super(Folder, self).permissions(user, inherited)
        perms.add('view')  # Grant everyone view access
        if user == self.user:
            perms.add('edit')
            perms.add('delete')
        return perms

    def __repr__(self):
        return u'<Folder %s>' % self.name

