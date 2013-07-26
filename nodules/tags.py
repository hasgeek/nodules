from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Tag, db
from .forms import EmptyForm, EditTagForm

tags_bp = Blueprint('tags', __name__)


@tags_bp.route('/')
def index():
    tags = Tag.query.order_by('created_at').all()
    return render_template('tags/index.html', tags=tags)


@tags_bp.route('/new', methods=['GET', 'POST'])
def new():
    ntf = EditTagForm()
    if ntf.validate_on_submit():
        tag = Tag()
        ntf.populate_obj(tag)
        tag.make_name()
        db.session.add(tag)
        db.session.commit()
        flash('Tag "%s" successfully created.' % tag.title)
        return redirect(url_for('tags.index'))
    return render_template('tags/edit.html', tag=None, form=ntf)


@tags_bp.route('/<tagname>')
def view(tagname):
    tag = Tag.query.filter_by(name=tagname).first_or_404()
    return render_template('tags/view.html', tag=tag)


@tags_bp.route('/<tagname>/edit', methods=['GET', 'POST'])
def edit(tagname):
    tag = Tag.query.filter_by(name=tagname).first_or_404()
    ef = EditTagForm(title=tag.title)
    if ef.validate_on_submit():
        ef.populate_obj(tag)
        db.session.commit()
        flash('Tag successfully renamed to "%s".' % tag.title)
        return redirect(url_for('tags.index'))
    return render_template('tags/edit.html', tag=tag, form=ef)


@tags_bp.route('/<tagname>/delete', methods=['GET', 'POST'])
def delete(tagname):
    tag = Tag.query.filter_by(name=tagname).first_or_404()
    df = EmptyForm()
    if df.validate_on_submit():
        db.session.delete(tag)
        db.session.commit()
        flash('Tag "%s" deleted.' % tag.title)
        return redirect(request.referrer)
    tag.type = 'Tag'
    return render_template('delete.html', node=tag, form=df)
