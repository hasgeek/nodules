# -*- coding: utf-8 -*-

from .models import *
from .views import *
from .forms import *


def init_app(app):
    from nodular import NodePublisher
    import nodules

    nodules.registry.register_node(PageType, view=PageView)
    app.pagepub = NodePublisher(app.root_node, nodules.registry, u'/')
