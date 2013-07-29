# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, flash

from nodular import NodeView
from nodules import db, registry, Node

from .models import Folder
from .forms import NewFolderForm

class FolderView(NodeView):
    @NodeView.route('/')
    def view(self):
        """ If the folder has a child named 'index', render that.
        Otherwise, show the listing of its children.
        """
        index_node = self.node.nodes.get('index')
        if index_node:
            view_cls = registry.nodeviews.get(index_node.type)[0]
            return view_cls(index_node).view()
        else:
            return render_template('folder/index.html', folder=self.node)


class NewFolderView(NodeView):
    @NodeView.route('/new/folder', methods=['GET', 'POST'])
    def newfolder(self):
        """ Render a form to make a new folder and show existing folders in it.
        """
        nf = NewFolderForm(request.form)
        if nf.validate_on_submit():
            f = Folder(name=nf.name.data, title=nf.title.data, parent=self.node)
            nf.populate_obj(f)
            db.session.commit()
            flash('Folder added with title "%s".' % nf.title.data)
            return redirect('/')
        folders = Folder.query.filter_by(parent=self.node).all()
        return render_template('folder/newfolder.html', form=nf, folders=folders)
