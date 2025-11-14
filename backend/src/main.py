from flask import Flask
from flask_cors import CORS

from src.config import config
from src.core.database import init_db,close_db


def create_app() -> Flask:

    app = Flask(__name__)
    app.config.from_object(config)
    
    # Enable CORS
    CORS(app)
    
    # Initialize database connection
    init_db(app)
    
    @app.route("/health")
    def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "database": "connected"}, 200
    
    @app.teardown_appcontext
    def close_db(error):
        """Close database session on app teardown."""
        close_db()
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=3000, debug=config.DEBUG)

