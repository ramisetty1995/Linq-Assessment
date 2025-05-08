import os

class Config:
    # Basic Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret')
    
    # Database Configuration (SQLite as the default)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///contact_notes.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Configuration
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # Token expires in 1 hour

    # Rate Limiting Configuration
    RATELIMIT_DEFAULT = "100 per minute"
    RATELIMIT_STORAGE_URI = "memory://"

    # Debug Configuration
    DEBUG = os.getenv('DEBUG', True)

    # Error Handling
    PROPAGATE_EXCEPTIONS = True

    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # CORS Configuration (if needed)
    CORS_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:5000"]

#import os

#class Config:
    #SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")
    #SQLALCHEMY_DATABASE_URI = "sqlite:///contact_notes.db"
    #SQLALCHEMY_TRACK_MODIFICATIONS = False
    #JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-secret")
    #RATE_LIMIT = "100 per minute"
    #OUTBOUND_TIMEOUT = 5