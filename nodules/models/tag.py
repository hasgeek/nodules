# -*- coding: utf-8 -*-

from coaster.sqlalchemy import BaseNameMixin
from nodules.models import db

node_tags = db.Table('node_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), nullable=False),
    db.Column('node_id', db.Integer, db.ForeignKey('node.id'), nullable=False),
)

class Tag(BaseNameMixin, db.Model):
    """
    Tags are used to categorize various nodes.
    A node can have zero or more tags.
    """
    __tablename__ = 'tag'
    nodes = db.relationship('Node', secondary='node_tags', lazy='dynamic',
                        backref=db.backref('tags'))


    def __init__(self, **kwargs):
        super(Tag, self).__init__(**kwargs)
        if not self.name:
            self.make_name()

    def __repr__(self):
        return "Tag <%s>" % (self.title)
