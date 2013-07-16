# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, flash

from nodular import NodeView, Node
from nodules import db, registry

from .models import Folder
from .forms import NewFolderForm

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


class NewFolderView(NodeView):
    @NodeView.route('/new/folder', methods=['GET', 'POST'])
    def index(self):
        nf = NewFolderForm(request.form)
        if nf.validate_on_submit():
            f = Folder(name=nf.name.data, title=nf.title.data, parent=self.node)
            nf.populate_obj(f)
            db.session.commit()
            flash('Folder added with title %s.' % nf.title.data)
            return redirect('/')
        folders = Folder.query.all()
        return render_template('folder/newfolder.html', form=nf, folders=folders)
