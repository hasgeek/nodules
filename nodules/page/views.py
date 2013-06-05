# -*- coding: utf-8 -*-

from nodular import NodeView

class PageView(NodeView):
    @NodeView.route('/')
    def index(self):
        return u'page index view'

    @NodeView.route('/edit', methods=['GET', 'POST'])
    @NodeView.route('/', methods=['PUT'])
    @NodeView.requires_permission('edit', 'siteadmin')
    def edit(self):
        return u'page edit view'

    @NodeView.route('/delete', methods=['GET', 'POST'])
    @NodeView.route('/', methods=['DELETE'])
    @NodeView.requires_permission('delete', 'siteadmin')
    def delete(self):
        return u'page delete view'
