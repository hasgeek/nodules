# -*- coding: utf-8 -*-

from .models import *
from .views import *
from .forms import *


def init_nodule(root, registry, pages_base_path='/'):
    """
    Publish the nodule and return the publisher
    """
    from nodular import NodePublisher

    registry.register_node(Page, view=PageView)
    pagepub = NodePublisher(root, registry, pages_base_path)
    return pagepub
