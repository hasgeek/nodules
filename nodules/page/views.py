# -*- coding: utf-8 -*-

from datetime import datetime
from flask import render_template, request, redirect, flash, jsonify, abort

from nodular import NodeView
from nodules.models import db
from nodules.forms import EmptyForm

from .forms import PageForm
from .models import Page

__all__ = ['PageView', 'NewPageView']

def make_response(request, response):
    if request.is_xhr:
        return jsonify(response)
    else:
        flash('Changes saved.')
        return redirect(response.get('path'))


class PageView(NodeView):
    @NodeView.route('/')
    def show(self):
        templ = self.node.template or 'show.html'
        pf, upf = EmptyForm(), EmptyForm()  # publish, unpublish forms
        return render_template('page/%s' % templ, page=self.node, pf=pf, upf=upf)

    @NodeView.route('/edit', methods=['GET', 'POST'])
    @NodeView.requires_permission('edit', 'siteadmin')
    def edit(self):
        form = PageForm(request.form, self.node)
        if form.validate_on_submit():
            form.populate_obj(self.node)
            db.session.commit()
            d = dict(status='success', path=self.node.path)
            return make_response(request, d)
        return render_template('page/edit.html', page=self.node, form=form)

    @NodeView.route('/delete', methods=['GET', 'POST'])
    @NodeView.requires_permission('delete', 'siteadmin')
    def delete(self):
        delete_form = EmptyForm()
        if delete_form.validate_on_submit():
            root_path = self.node.root.path
            db.session.delete(self.node)
            db.session.commit()
            return redirect(root_path)
        return render_template('delete.html', node=self.node, form=delete_form)

    @NodeView.route('/<action>', methods=['POST'])
    @NodeView.requires_permission('publish', 'siteadmin')
    def publish(self, action):
        if not action in ('publish', 'unpublish'):
            abort(404)
        form = EmptyForm()
        if form.validate_on_submit():
            if action == 'publish':
                flash('Page published.')
                self.node.published_at = datetime.now()
            else:
                flash('This page is now a draft.')
                self.node.published_at = None
            db.session.commit()
            return redirect(self.node.path)
        return redirect(request.referrer)


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
            d = dict(status='success', path=p.path)
            return make_response(request, d)
        return render_template('page/edit.html', page=p, page_form=pf)
