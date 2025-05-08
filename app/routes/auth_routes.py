from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User
from app.schemas.user_schema import UserSchema, LoginSchema
from flask_jwt_extended import create_access_token

bp = Blueprint('auth', __name__, url_prefix="/api/auth")

user_schema = UserSchema()
login_schema = LoginSchema()

@bp.route('/register', methods=['POST'])
def register():
    print("Hello Register POST")
    print(request)
    input = request.form
    print(f"Type: {type(input)}")
    print(input)
    data = {}
    try:
        data['username'] = request.form['username']
        data['password'] = request.form['password']
    except Exception as e:
        print(type(e))
        print(e)
        raise e
    print("Step-2")
    print(f"Data: {data}")
    errors = user_schema.validate(data)
    print(f"Errors: {errors}")
    if errors:
        return jsonify(errors), 400
    print("All-Good-1")
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "Username already exists"}), 409
    print("All Good-2")
    user = User(username=data['username'])
    user.set_password(data['password'])
    print("All Good-3")
    db.session.add(user)
    db.session.commit()
    print("All Good-4")
    return jsonify({"message": "User registered successfully"}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    errors = login_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Invalid credentials"}), 401