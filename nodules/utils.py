# -*- coding: utf-8 -*-

from datetime import datetime
from flask import redirect, flash
from nodules import db, registry

from .forms import EmptyForm

def change_publish_status(node, status):
    """
    Publish the `node` if `status` is True else unpublish it.
    """
    form = EmptyForm()
    if form.validate_on_submit():
        if status:
            node.published_at = datetime.now()
            msg = 'Page published.'
        else:
            node.published_at = None
            msg = 'This page is now a draft.'
        db.session.commit()
        flash(msg)
        return redirect(registry.url_for(node, 'view'))
    return redirect(request.referrer)

