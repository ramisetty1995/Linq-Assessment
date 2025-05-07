from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.contact import Contact
from app.models.note import Note
from app.schemas.note_schema import NoteSchema

bp = Blueprint('notes', __name__, url_prefix="/api/notes")

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)

@bp.route("/", methods=["POST"])
@jwt_required()
def create_note():
    current_user = get_jwt_identity()
    data = request.get_json()
    errors = note_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    contact = Contact.query.filter_by(id=data['contact_id'], user_id=current_user).first()
    if not contact:
        return jsonify({"message": "Contact not found or unauthorized"}), 404
    note = Note(content=data['content'], contact_id=contact.id)
    db.session.add(note)
    db.session.commit()
    return note_schema.jsonify(note), 201

@bp.route("/contact/<int:contact_id>", methods=["GET"])
@jwt_required()
def get_notes_for_contact(contact_id):
    current_user = get_jwt_identity()
    contact = Contact.query.filter_by(id=contact_id, user_id=current_user).first()
    if not contact:
        return jsonify({"message": "Contact not found"}), 404

    notes = Note.query.filter_by(contact_id=contact.id).all()
    return notes_schema.jsonify(notes), 200

@bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_note(id):
    current_user = get_jwt_identity()
    note = db.session.query(Note).join(Contact).filter(
        Note.id == id,
        Contact.user_id == current_user
    ).first()

    if not note:
        return jsonify({"message": "Note not found"}), 404

    data = request.get_json()
    errors = note_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400

    note.content = data.get('content', note.content)
    db.session.commit()
    return note_schema.jsonify(note), 200

@bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_note(id):
    current_user = get_jwt_identity()
    note = db.session.query(Note).join(Contact).filter(
        Note.id == id,
        Contact.user_id == current_user
    ).first()

    if not note:
        return jsonify({"message": "Note not found"}), 404

    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": "Note deleted"}), 200