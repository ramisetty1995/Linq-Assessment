from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from flask_jwt_extended import JWTManager
from .config import Config
from .extensions import db, ma, limiter
from .models import user, contact, note
from .routes import auth_routes, contact_routes, note_routes
from .swagger import swagger_template, swagger_contact_paths

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Temporary hardcoding to check
    app.config['JWT_SECRET_KEY'] = 'jwt-secret'  # Hardcoded key
    print(f"Loaded JWT Secret Key: {app.config['JWT_SECRET_KEY']}")  # Debug statement

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    jwt = JWTManager(app)

    # Swagger setup
    SWAGGER_URL = '/swagger'
    API_URL = '/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    @app.route(API_URL)
    def swagger_json():
        swag = swagger_template()
        swag['paths'].update(swagger_contact_paths())
        return jsonify(swag)


    # Registering the Blueprints
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(contact_routes.bp)
    app.register_blueprint(note_routes.bp)

    @app.route('/')
    @app.route('/favicon.ico')
    def home():
        return jsonify({"message": "Welcome to the Contact Notes API!"}), 200

    # Error Handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"message": "Resource not found"}), 404

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({"message": "Unauthorized access"}), 401

    @app.errorhandler(429)
    def rate_limit_exceeded(e):
        return jsonify({"message": "Rate limit exceeded. Try again later."}), 429

    @app.errorhandler(Exception)
    def internal_error(e):
        return jsonify({"message": "An internal error occurred."}), 500

    # Create Database Tables
    with app.app_context():
        db.create_all()
        return app