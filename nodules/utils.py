# -*- coding: utf-8 -*-

from datetime import datetime
from flask import redirect, flash

from nodules import db, rootpub
from .models import Tag
import forms

def change_publish_status(node, status):
    """
    Publish the `node` if `status` is True else unpublish it.
    """
    form = forms.EmptyForm()
    if form.validate_on_submit():
        if status:
            node.published_at = datetime.now()
            msg = 'Page published.'
        else:
            node.published_at = None
            msg = 'This page is now a draft.'
        db.session.commit()
        flash(msg)
        return redirect(rootpub.url_for(node, 'view'))
    return redirect(request.referrer)


def get_all_tags():
    return [t.name for t in Tag.query.all()]


def get_or_make_tag(title):
    tag = Tag.query.filter_by(title=title).first()
    if not tag:
        tag = Tag(title=title)
        tag.make_name()
        db.session.add(tag)
    return tag
