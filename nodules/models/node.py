# -*- coding: utf-8 -*-

from nodular import Node
from werkzeug import cached_property

# Monkey patch the `template` and `theme` into Node 

def template(self):
    """View template of the node."""
    return self.properties.get('template')


def theme(self):
    """Theme of the node or that of any parent node."""
    return self.getprop('theme')


Node.template = cached_property(template)
Node.theme = cached_property(theme)
