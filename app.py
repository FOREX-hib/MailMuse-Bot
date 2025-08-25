"""
Flask web application for Telegram Bot Dashboard
"""
import os
import logging
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from extensions import db
from routes import register_routes

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def create_app():
    """Application factory pattern"""
    # Create the app
    app = Flask(__name__)
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Configure the database
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///telegram_bot.db")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize the app with the extension
    db.init_app(app)

    # Import models first, before creating tables
    import models  # noqa: F401

    with app.app_context():
        # Create all tables
        db.create_all()
        logging.info("Database tables created successfully")

    # Register routes
    register_routes(app)
    
    return app

# Create app instance
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)