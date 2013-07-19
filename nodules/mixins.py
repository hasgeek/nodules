# -*- coding: utf-8 -*-

from werkzeug.routing import Map as UrlMap, Rule as UrlRule

from nodular import NodeView
from .utils import change_publish_status


class PublishMixin(object):
    """
    Provides publish and unpublish endpoints.
    """
    url_map = UrlMap([
                   UrlRule('/publish', methods=['POST'], endpoint='publish'),
                   UrlRule('/unpublish', methods=['POST'], endpoint='unpublish')
               ], strict_slashes=False)

    @NodeView.requires_permission('publish', 'siteadmin')
    def publish(self):
        return change_publish_status(self.node, status=True)

    @NodeView.requires_permission('publish', 'siteadmin')
    def unpublish(self):
        return change_publish_status(self.node, status=False)

    view_functions = dict(publish=publish, unpublish=unpublish)
