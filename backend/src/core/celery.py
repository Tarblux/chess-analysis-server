"""Celery application instance and RabbitMQ connection management."""
from celery import Celery

from src.config import config
from src.utils.decorators import safe_init

# Global Celery app instance
celery_app = None


@safe_init(service_name="Celery")
def init_celery(app_name: str = "elombe") -> Celery:
    """
    Initialize Celery application with RabbitMQ broker.
    
    Args:
        app_name: Name of the Celery application
    
    Returns:
        Celery application instance
    """
    global celery_app
    
    celery_app = Celery(
        app_name,
        broker=config.RABBITMQ_BROKER_URL,
        backend=config.RABBITMQ_BROKER_URL  # Using same broker as backend for now
    )
    
    celery_app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
    )
    
    return celery_app


def check_rabbitmq_health() -> tuple[bool, str]:
    """
    Check RabbitMQ connection health via Celery's broker connection.
    
    Returns:
        Tuple of (is_healthy, message)
    """
    if celery_app is None:
        return False, "Celery app not initialized"
    
    try:
        # Use Celery's connection pool to check Brabbit Connection
        conn = celery_app.connection()
        conn.ensure_connection(max_retries=1)
        conn.release()
        return True, "Connection successful"
    except Exception as e:
        return False, f"Connection failed: {str(e)}"


def get_celery_app() -> Celery:
    """
    Get Celery application instance.
    
    Returns:
        Celery application instance
    
    Raises:
        RuntimeError: If Celery app not initialized
    """
    if celery_app is None:
        raise RuntimeError("Celery not initialized. Call init_celery() first.")
    return celery_app

