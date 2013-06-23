# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, flash

from nodular import NodeView, Node
from nodules import db, registry


class FolderView(NodeView):
    @NodeView.route('/')
    def index(self):
        index_node = Node.query.filter_by(parent=self.node, name='index').first()
        if index_node:
            view_cls = registry.nodeviews.get(index_node.type)[0]
            return view_cls(index_node).show()
        else:
            children = Node.query.filter_by(parent=self.node)
            return render_template('folder/index.html', children=children)
