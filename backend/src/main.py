from flask import Flask
from flask_cors import CORS
import time

from src.config import config
from src.core.database import init_db, close_db
from src.core.neo4j import init_neo4j, close_neo4j
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
    
    # Initialize database connections
    try:
        init_db(app)
    except Exception as e:
        app.logger.warning(f"Database initialization failed: {e}. App will continue without database.")
    
    # Initialize Neo4j
    try:
        init_neo4j(app)
    except Exception as e:
        app.logger.warning(f"Neo4j initialization failed: {e}. App will continue without Neo4j.")
    
    # Initialize Celery 
    try:
        init_celery()
    except Exception as e:
        app.logger.warning(f"Celery initialization failed: {e}. App will continue without Celery.")
    
    # Register health check routes
    app.register_blueprint(health_bp)
    
    @app.teardown_appcontext
    def teardown_db(error):
        """Close database session on app teardown."""
        close_db()
    
    @app.teardown_appcontext
    def teardown_neo4j(error):
        """Close Neo4j connection on app teardown."""
        close_neo4j()
    
    return app


# Create app instance for Gunicorn WSGI server (Gunicorn expects a WSGI callable (the Flask app), not the factory function)
app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5150, debug=config.DEBUG)

