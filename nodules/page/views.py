# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, flash

from nodular import NodeView
from nodules.models import db

from .forms import PageForm
from .models import PageType


class PageView(NodeView):
    @NodeView.route('/')
    def index(self):
        return render_template('page/show.html', page=self.node)

    @NodeView.route('/edit', methods=['GET', 'POST'])
    @NodeView.requires_permission('edit', 'siteadmin')
    def edit(self):
        form = PageForm(request.form, self.node)
        if form.validate_on_submit():
            form.populate_obj(self.node)
            self.node.make_name()
            db.session.commit()
            flash('Changes saved.')
            return redirect(self.node.path)
        return render_template('page/edit.html', page=self.node, form=form)

    @NodeView.route('/delete', methods=['GET', 'POST'])
    @NodeView.requires_permission('delete', 'siteadmin')
    def delete(self):
        if request.method == 'POST':
            root_path = self.node.root.path
            self.node.delete()
        return redirect(root_path)
