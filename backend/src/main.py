from flask import Flask
from flask_cors import CORS
import time

from src.config import config
from src.core.database import init_db, close_db
from src.core.neo4j import init_neo4j
from src.core.celery import init_celery
from src.api.routes import health_bp

# Track app start time for uptime calculation
_app_start_time = time.time()


def create_app() -> Flask:

    app = Flask(__name__)
    app.config.from_object(config)
    
    # Store app start time in app config for health checks
    app.config["start_time"] = _app_start_time
    
    # Enable CORS
    CORS(app)
    
    # Initialize infra connections (PostgreSQL,Neo4j,Celery)
    init_db(app)
    init_neo4j(app)
    init_celery()
    
    # Register health check routes
    app.register_blueprint(health_bp)
    
    @app.teardown_appcontext
    def teardown_db(error):
        """Close database session on app teardown and after request."""
        close_db()
    
    return app


# Create app instance for Gunicorn WSGI server (Gunicorn expects a WSGI callable (the Flask app), not the factory function like I had before)
app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5150, debug=config.DEBUG)

