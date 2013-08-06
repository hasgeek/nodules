# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, flash, jsonify, abort

from nodular import NodeView
from nodules import db, rootpub
from nodules.forms import EmptyForm
from nodules.mixins import PublishMixin, DeleteMixin

from .forms import MetaForm
from .models import Form

__all__ = ['FormView', 'NewFormView']

def make_response(request, response):
    if request.is_xhr:
        return jsonify(response)
    else:
        flash('Changes saved.')
        return redirect(response.get('path'))


class FormView(NodeView, PublishMixin, DeleteMixin):
    @NodeView.route('/')
    def view(self):
        templ = self.node.template or 'view.html'
        pf, upf = EmptyForm(), EmptyForm()  # publish, unpublish forms
        return render_template('form/%s' % templ, form=self.node, pf=pf, upf=upf)

    @NodeView.route('/edit', methods=['GET', 'POST'])
    @NodeView.requires_permission('edit', 'siteadmin')
    def edit(self):
        form = MetaForm(request.form, self.node)
        if form.validate_on_submit():
            form.populate_obj(self.node)
            db.session.commit()
            d = dict(status='success', path=self.node.path)
            return make_response(request, d)
        choice_00 = form.questions[0].choices[0]
        return render_template('form/edit.html', node=self.node, form=form, choice_00=choice_00)


class NewFormView(NodeView):
    """New form view to be attached to container node.
    """
    @NodeView.route('/new/form', methods=['GET', 'POST'])
    def newform(self):
        mf = MetaForm(request.form)
        f = Form(parent=self.node)

        if mf.validate_on_submit():
            mf.populate_obj(f)
            f.make_name()
            db.session.commit()
            d = dict(status='success', path=f.path)
            return make_response(request, d)
        choice_00 = mf.questions[0].choices.append_entry()
        return render_template('form/edit.html', node=f, form=mf, choice_00=choice_00)
