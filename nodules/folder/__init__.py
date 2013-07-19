# -*- coding: utf-8 -*-

from .models import *
from .views import *
from .forms import *

from nodules.page import NewPageView

def init_nodule(root, registry, base_path='/', urlpath=None):
    """
    Publish the nodule and return the publisher
    """
    from nodular import NodePublisher
    registry.register_node(Folder, view=FolderView, child_nodetypes=['*'], parent_nodetypes=['*'])
    registry.register_view(Folder, NewPageView)
    registry.register_view(Folder, NewFolderView)
    folder_pub = NodePublisher(root, registry, base_path, urlpath)
    return folder_pub
