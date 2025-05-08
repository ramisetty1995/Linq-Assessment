from app.extensions import limiter
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.contact import Contact
from app.schemas.contact_schema import ContactSchema
from app.utils import normalize_note_fields

bp = Blueprint('contacts', __name__, url_prefix="/api/contacts")

contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)

@bp.route("/", methods=["POST"])
@jwt_required()
@limiter.limit("10 per minute")
def create_contact():
    user_id = get_jwt_identity()
    data = normalize_note_fields(request.get_json())
    
    errors = contact_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Check for existing contact with the same email
    if Contact.query.filter_by(email=data['email'], user_id=user_id).first():
        return jsonify({"message": "Contact with this email already exists."}), 409

    contact = Contact(
        full_name=data['full_name'],
        email=data['email'],
        phone=data.get('phone'),
        user_id=user_id
    )
    db.session.add(contact)
    db.session.commit()
    return contact_schema.jsonify(contact), 201

# Get all contacts for the authenticated user
@bp.route("/", methods=["GET"])
@jwt_required()
def get_contacts():
    user_id = get_jwt_identity()
    contacts = Contact.query.filter_by(user_id=user_id).all()
    return contacts_schema.jsonify(contacts), 200

# Get a single contact by ID
@bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_contact(id):
    user_id = get_jwt_identity()
    contact = Contact.query.filter_by(id=id, user_id=user_id).first()
    if not contact:
        return jsonify({"message": "Contact not found"}), 404
    return contact_schema.jsonify(contact), 200

# Update an existing contact
@bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_contact(id):
    user_id = get_jwt_identity()
    contact = Contact.query.filter_by(id=id, user_id=user_id).first()
    if not contact:
        return jsonify({"message": "Contact not found"}), 404

    data = normalize_note_fields(request.get_json())
    errors = contact_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400

    # Update contact fields
    contact.full_name = data.get('full_name', contact.full_name)
    contact.email = data.get('email', contact.email)
    contact.phone = data.get('phone', contact.phone)

    db.session.commit()
    return contact_schema.jsonify(contact), 200

# Delete a contact
@bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_contact(id):
    user_id = get_jwt_identity()
    contact = Contact.query.filter_by(id=id, user_id=user_id).first()
    if not contact:
        return jsonify({"message": "Contact not found"}), 404

    db.session.delete(contact)
    db.session.commit()
    return jsonify({"message": "Contact deleted"}), 200