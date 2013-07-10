# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, flash, jsonify

from nodular import NodeView
from nodules.models import db
from nodules.forms import DeleteForm

from .forms import PageForm
from .models import Page

__all__ = ['PageView', 'NewPageView']

class PageView(NodeView):
    @NodeView.route('/')
    def show(self):
        templ = self.node.template or 'show.html'
        return render_template('page/%s' % templ, page=self.node)

    @NodeView.route('/edit', methods=['GET', 'POST'])
    @NodeView.requires_permission('edit', 'siteadmin')
    def edit(self):
        form = PageForm(request.form, self.node)
        if form.validate_on_submit():
            form.populate_obj(self.node)
            db.session.commit()
            if request.is_xhr:
                return jsonify({'status': 'success', 'path': self.node.path})
            else:
                flash('Changes saved.')
                return redirect(self.node.path)
        return render_template('page/edit.html', page=self.node, form=form)

    @NodeView.route('/delete', methods=['GET', 'POST'])
    @NodeView.requires_permission('delete', 'siteadmin')
    def delete(self):
        form = DeleteForm()
        if form.validate_on_submit():
            root_path = self.node.root.path
            db.session.delete(self.node)
            db.session.commit()
            return redirect(root_path)
        return render_template('delete.html', node=self.node, form=form)


class NewPageView(NodeView):
    """New page view to be attached to Container node.
       e.g., folder - self.node.type would be `folder`.
    """
    @NodeView.route('/new/page', methods=['GET', 'POST'])
    def new(self):
        pf = PageForm(request.form)
        p = Page(parent=self.node)
        if pf.validate_on_submit():
            pf.populate_obj(p)
            db.session.commit()
            if request.is_xhr:
                return jsonify({'status': 'success', 'path': p.path})
            else:
                flash('Changes saved.')
                return redirect(p.path)
        return render_template('page/edit.html', page=p, form=pf)
