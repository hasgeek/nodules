# -*- coding: utf-8 -*-

import json
import sqlalchemy.types as types

from nodular import NodeMixin
from nodules import db, Node


# http://www.sqlalchemy.org/docs/core/types.html#custom-types
class JsonType(types.TypeDecorator):
    impl = types.UnicodeText
    def process_bind_param(self, value, dialect):
        if value is not None:
            value = unicode(json.dumps(value))
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        else:
            return {}


class Form(NodeMixin, Node):
    __tablename__ = 'form'

    description = db.Column(db.UnicodeText)
    questions = db.Column(JsonType)
    # accepting_responses = db.Column(db.Boolean)

    def __init__(self, **kwargs):
        super(Form, self).__init__(**kwargs)
        if self.title and not self.name:
            self.make_name()

    def permissions(self, user, inherited=None):
        perms = super(Form, self).permissions(user, inherited)
        perms.add('view')  # Grant everyone view access
        if user == self.user:
            perms.add('edit')
            perms.add('publish')
            perms.add('delete')
        return perms

    def __repr__(self):
        return u'<Form %s>' % self.name

