# -*- coding: utf-8 -*-

from __future__ import absolute_import

from ._version import *

import os.path, jinja2

from nodular import NodeRegistry, Node

# Import basic nodes like User

from nodules.models import User, db

# Do not import content nodes until they are required by the client app
