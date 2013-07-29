# -*- coding: utf-8 -*-

from __future__ import absolute_import

from ._version import *

import os.path, jinja2

from nodular import NodeRegistry, NodePublisher

# get the monkey patched Node with theme and template
from nodules.models.node import Node

# Import basic nodes like User
from nodules.models import User, db

# Do not import content nodes until they are required by the client app

registry = NodeRegistry()
rootpub = NodePublisher(None, registry, basepath='/') # call `init_root` on it in the app.
