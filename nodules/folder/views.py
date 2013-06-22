# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, flash

from nodular import NodeView, Node
from nodules import db, registry


class FolderView(NodeView):
    @NodeView.route('/blah')
    def index(self):
        index_node = Node.query.filter_by(parent=self.node, name='index').first()
        if index_node:
            # fix me: this shouldn't be redirect
            return redirect(index_node.path)
        else:
            children = Node.query.filter_by(parent=self.node)
            return render_template('folder/index.html', children=children)

    @NodeView.route('/delete', methods=['GET', 'POST'])
    @NodeView.requires_permission('delete', 'siteadmin')
    def delete(self):
        if request.method == 'POST':
            root_path = self.node.root.path
            self.node.delete()
        return redirect(root_path)
