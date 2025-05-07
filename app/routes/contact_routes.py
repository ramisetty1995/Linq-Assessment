from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.contact import Contact
from app.schemas.contact_schema import ContactSchema

bp = Blueprint('contacts', __name__, url_prefix="/api/contacts")

contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)

@bp.route("/", methods=["POST"])
@jwt_required()
def create_contact():
    current_user = get_jwt_identity()
    data = request.get_json()
    errors = contact_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    contact = Contact(
        full_name=data['full_name'],
        email=data['email'],
        phone=data.get('phone'),
        user_id=current_user
    )
    db.session.add(contact)
    db.session.commit()
    return contact_schema.jsonify(contact), 201

@bp.route("/", methods=["GET"])
@jwt_required()
def get_contacts():
    current_user = get_jwt_identity()
    contacts = Contact.query.filter_by(user_id=current_user).all()
    return contacts_schema.jsonify(contacts), 200

@bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_contact(id):
    current_user = get_jwt_identity()
    contact = Contact.query.filter_by(id=id, user_id=current_user).first()
    if not contact:
        return jsonify({"message": "Contact not found"}), 404
    return contact_schema.jsonify(contact), 200

@bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_contact(id):
    current_user = get_jwt_identity()
    contact = Contact.query.filter_by(id=id, user_id=current_user).first()
    if not contact:
        return jsonify({"message": "Contact not found"}), 404

    data = request.get_json()
    errors = contact_schema.validate(data, partial=True)
    if errors:
        return jsonify(errors), 400

    contact.full_name = data.get('full_name', contact.full_name)
    contact.email = data.get('email', contact.email)
    contact.phone = data.get('phone', contact.phone)

    db.session.commit()
    return contact_schema.jsonify(contact), 200

@bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_contact(id):
    current_user = get_jwt_identity()
    contact = Contact.query.filter_by(id=id, user_id=current_user).first()
    if not contact:
        return jsonify({"message": "Contact not found"}), 404

    db.session.delete(contact)
    db.session.commit()
    return jsonify({"message": "Contact deleted"}), 200