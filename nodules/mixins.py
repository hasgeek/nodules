# -*- coding: utf-8 -*-

from werkzeug.routing import Map as UrlMap, Rule as UrlRule
from flask import redirect, flash, render_template

from nodular import NodeView

from nodules import db, rootpub
from .forms import EmptyForm
from .utils import change_publish_status

__all__ = ['PublishMixin', 'DeleteMixin']


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


class DeleteMixin(object):
    """
    Provides delete endpoint
    """
    url_map = UrlMap([UrlRule('/delete', methods=['GET', 'POST'], endpoint='delete')],
                        strict_slashes=False)

    @NodeView.requires_permission('delete', 'siteadmin')
    def delete(self):
       delete_form = EmptyForm()
       if delete_form.validate_on_submit():
           db.session.delete(self.node)
           db.session.commit()
           flash('%s "%s" deleted.' % (self.node.type.title(), self.node.title))
           return redirect(rootpub.url_for(self.node.parent))
       return render_template('delete.html', node=self.node, form=delete_form)

    view_functions = dict(delete=delete)
