# -*- coding: utf-8 -*-

from .models import *
from .views import *
from .forms import *


def init_nodule(root, registry, base_path='/'):
    """
    Publish the nodule and return the publisher
    """
    from nodular import NodePublisher
    registry.register_node(Folder, view=FolderView, child_nodetypes=['*'], parent_nodetypes=['*'])
    folder_pub = NodePublisher(root, registry, base_path)
    return folder_pub
