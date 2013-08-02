# -*- coding: utf-8 -*-

from .models import *
from .views import *
from .forms import *

def init_nodule(root, registry, base_path='/', urlpath=None):
    registry.register_node(Form, view=FormView, child_nodetypes=['*'], parent_nodetypes=['*'])
