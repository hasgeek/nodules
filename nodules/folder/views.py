# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, flash

from nodular import NodeView, Node
from nodules import db, registry

class FolderView(NodeView):
    # to be improved
    @NodeView.route('/index')
    def index(self):
        children = Node.query.filter_by(parent=self.node)
        return render_template('folder/index.html', children=children)

    @NodeView.route('/delete', methods=['GET', 'POST'])
    @NodeView.requires_permission('delete', 'siteadmin')
    def delete(self):
        if request.method == 'POST':
            root_path = self.node.root.path
            self.node.delete()
        return redirect(root_path)
