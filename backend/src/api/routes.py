"""Health check route handlers."""
from flask import Blueprint, jsonify, current_app
from datetime import datetime, timezone
import time

from src.config import config
from src.core.database import check_db_health
from src.core.neo4j import check_neo4j_health
from src.core.celery import check_rabbitmq_health

# Create blueprint for health check routes
health_bp = Blueprint("health", __name__)


def _format_uptime(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours}h {minutes}m {seconds}s"


@health_bp.route("/health")
def health_check():
    """Comprehensive health check endpoint with service status and metadata."""
    # Check all services
    db_healthy, db_message = check_db_health()
    neo4j_healthy, neo4j_message = check_neo4j_health()
    rabbitmq_healthy, rabbitmq_message = check_rabbitmq_health()
    
    # Determine overall status (healthy if all services are healthy)
    overall_healthy = db_healthy and neo4j_healthy and rabbitmq_healthy
    
    # Calculate uptime
    start_time = current_app.config.get("start_time", time.time())
    uptime_seconds = time.time() - start_time
    uptime_str = _format_uptime(uptime_seconds)
    
    # Get current timestamp in ISO format
    now = datetime.now(timezone.utc)
    timestamp = now.isoformat().replace("+00:00", "Z")
    
    # Determine database connection status
    database_status = "connected" if db_healthy else "disconnected"
    
    response = {
        "status": "healthy" if overall_healthy else "unhealthy",
        "database": database_status,
        "timestamp": timestamp,
        "appVersion": config.APP_VERSION,
        "uptime": uptime_str,
        "environment": config.ENVIRONMENT,
        "serverTime": timestamp,
        "services": {
            "postgresql": {
                "status": "healthy" if db_healthy else "unhealthy",
                "message": db_message
            },
            "neo4j": {
                "status": "healthy" if neo4j_healthy else "unhealthy",
                "message": neo4j_message
            },
            "rabbitmq": {
                "status": "healthy" if rabbitmq_healthy else "unhealthy",
                "message": rabbitmq_message
            }
        }
    }
    
    status_code = 200 if overall_healthy else 503
    return jsonify(response), status_code


@health_bp.route("/health/db")
def health_check_db():
    """PostgreSQL database health check endpoint."""
    is_healthy, message = check_db_health()
    
    status_code = 200 if is_healthy else 503
    return jsonify({
        "status": "healthy" if is_healthy else "unhealthy",
        "service": "postgresql",
        "message": message
    }), status_code


@health_bp.route("/health/neo4j")
def health_check_neo4j():
    """Neo4j graph database health check endpoint."""
    is_healthy, message = check_neo4j_health()
    
    status_code = 200 if is_healthy else 503
    return jsonify({
        "status": "healthy" if is_healthy else "unhealthy",
        "service": "neo4j",
        "message": message
    }), status_code


@health_bp.route("/health/queue")
def health_check_queue():
    """RabbitMQ message queue health check endpoint."""
    is_healthy, message = check_rabbitmq_health()
    
    status_code = 200 if is_healthy else 503
    return jsonify({
        "status": "healthy" if is_healthy else "unhealthy",
        "service": "rabbitmq",
        "message": message
    }), status_code

