# -*- coding: utf-8 -*-

from .models import *
from .views import *
from .forms import *


def init_nodule(root, registry, base_path='/', urlpath=None):
    """
    Publish the nodule and return the publisher
    """
    from nodular import NodePublisher

    registry.register_node(Page, view=PageView, parent_nodetypes=['*'])
    pagepub = NodePublisher(root, registry, base_path, urlpath)
    return pagepub
