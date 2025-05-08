from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from .config import Config
from .extensions import db, ma, limiter
from .models import user, contact, note
from .routes import auth_routes, contact_routes, note_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    ma.init_app(app)
    limiter.init_app(app)

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