from flask import Flask
from .config import Config
from .extensions import db, jwt, ma
from .models import user, contact, note
from .routes import auth_routes, contact_routes, note_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(contact_routes.bp)
    app.register_blueprint(note_routes.bp)

    with app.app_context():
        db.create_all()

    return app