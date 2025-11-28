"""Decorators for safe initialization and error handling."""
from functools import wraps
from typing import Callable, Any, Optional
import logging
from flask import Flask

# Default logger for cases where Flask app logger is not available
_default_logger = logging.getLogger(__name__)


def safe_init(service_name: Optional[str] = None):
    """
    Decorator that wraps initialization functions with try-except blocks
    for graceful error handling during service initialization.
    
    If initialization fails, logs a warning and returns None instead of raising.
    This allows the application to continue running even if some services
    are unavailable during startup.
    
    Args:
        service_name: Name of the service being initialized (e.g., "Database", "Neo4j", "Celery").
                     If not provided, will attempt to infer from function name.
    
    Example:
        @safe_init(service_name="Database")
        def init_db(app: Flask) -> None:
            # initialization code
    
        @safe_init(service_name="Celery")
        def init_celery(app_name: str = "elombe") -> Celery:
            # initialization code
    """
    def decorator(func: Callable) -> Callable:
        # Determine service name if not provided
        name = service_name or func.__name__.replace("init_", "").replace("_", " ").title()
        
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Try to get Flask app logger from args
            logger = _default_logger
            for arg in args:
                if isinstance(arg, Flask):
                    logger = arg.logger
                    break
            
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.warning(
                    f"{name} initialization failed: {e}. "
                    f"App will continue without {name}."
                )
                return None
        
        return wrapper
    return decorator

