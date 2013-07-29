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


def get_or_make_tags(titles):
    titles = set(titles)
    existing_tags = Tag.query.filter(Tag.title.in_(titles)).all()
    existing_titles = set(t.title for t in existing_tags)
    newtags = []
    for title in titles - existing_titles:
        tag = Tag(title=title)
        tag.make_name()
        newtags.append(tag)
    db.session.add_all(newtags)
    return existing_tags + newtags
