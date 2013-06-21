# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, flash

from nodular import NodeView, Node
from nodules.models import db

from nodules.page import PageForm, Page


class FolderView(NodeView):
    # to be improved
    @NodeView.route('/index')
    def index(self):
        children = Node.query.filter_by(parent=self.node)
        return render_template('folder/index.html', children=children)

    @NodeView.route('/new/<nodule>', methods=['GET', 'POST'])
    @NodeView.requires_permission('edit', 'siteadmin')
    def new(self, nodule):
        if nodule == 'page':
            pf = PageForm(request.form)
            p = Page(parent=self.node)
            if pf.validate_on_submit():
                pf.populate_obj(p)
                p.make_name()
                db.session.commit()
                flash('Changes saved.')
                return redirect(p.path)
            return render_template('page/edit.html', page=None, form=pf)
        else:
            raise NotImplementedError

    @NodeView.route('/delete', methods=['GET', 'POST'])
    @NodeView.requires_permission('delete', 'siteadmin')
    def delete(self):
        if request.method == 'POST':
            root_path = self.node.root.path
            self.node.delete()
        return redirect(root_path)
