from flask import render_template, request, jsonify, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app import db
from app.notes import notes
from app.models import Note
from app.forms import NoteForm

@notes.route('/')
@login_required                         
def index():
    user_notes = Note.query.filter_by(user_id=current_user.id)\
                           .order_by(Note.created_at.desc()).all()
    form = NoteForm()
    return render_template('notes/index.html', notes=user_notes, form=form)


@notes.route('/notes', methods=['POST'])
@login_required
def create():
    form = NoteForm()
    if form.validate_on_submit():
        note = Note(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id
        )
        db.session.add(note)
        db.session.commit()
        flash('Note saved!', 'success')
    return redirect(url_for('notes.index'))


@notes.route('/notes/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    note = Note.query.get_or_404(id)
    if note.user_id != current_user.id:
        abort(403)                       
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted.', 'info')
    return redirect(url_for('notes.index'))


@notes.route('/api/notes', methods=['GET'])
@login_required
def api_list():
    user_notes = Note.query.filter_by(user_id=current_user.id).all()
    return jsonify([n.to_dict() for n in user_notes])


@notes.route('/api/notes', methods=['POST'])
@login_required
def api_create():
    data = request.get_json()
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({'error': 'title and content required'}), 400
    note = Note(title=data['title'], content=data['content'], user_id=current_user.id)
    db.session.add(note)
    db.session.commit()
    return jsonify(note.to_dict()), 201


@notes.route('/api/notes/<int:id>', methods=['DELETE'])
@login_required
def api_delete(id):
    note = Note.query.get_or_404(id)
    if note.user_id != current_user.id:
        return jsonify({'error': 'forbidden'}), 403
    db.session.delete(note)
    db.session.commit()
    return jsonify({'deleted': True})