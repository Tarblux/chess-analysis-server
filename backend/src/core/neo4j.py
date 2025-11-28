"""Neo4j graph database connection and session management."""
from flask import Flask
from neo4j import GraphDatabase

from src.config import config
from src.utils.decorators import safe_init

# Global Neo4j driver instance
driver = None


@safe_init(service_name="Neo4j")
def init_neo4j(app: Flask) -> None:
    """
    Initialize Neo4j database connection
    
    Args:
        app: Flask application instance
    """
    global driver
    
    # Validate required config values
    if not config.NEO4J_USER or not config.NEO4J_PASSWORD:
        raise ValueError("NEO4J_USER and NEO4J_PASSWORD must be set in environment variables")
    
    # Create Neo4j driver
    driver = GraphDatabase.driver(
        config.NEO4J_URI,
        auth=(config.NEO4J_USER, config.NEO4J_PASSWORD)
    )
    
    # Test connection
    try:
        database = config.NEO4J_DATABASE or "neo4j"
        with driver.session(database=database) as session:
            session.run("RETURN 1")
        app.logger.info(f"Successfully connected to Neo4j: {config.NEO4J_URI}")
    except Exception as e:
        error_msg = str(e)
        app.logger.error(f"Failed to connect to Neo4j: {error_msg}")
        raise


def get_neo4j_session(database: str | None = None):
    """
    Get Neo4j database session.
    
    Args:
        database: Database name (defaults to config.NEO4J_DATABASE or "neo4j")
    
    Yields:
        Neo4j session
    """
    if driver is None:
        raise RuntimeError("Neo4j not initialized. Call init_neo4j() first.")
    
    db = database or config.NEO4J_DATABASE or "neo4j"
    session = driver.session(database=db)
    try:
        yield session
    finally:
        session.close()


def check_neo4j_health() -> tuple[bool, str]:
    """
    Check Neo4j connection health.
    
    Returns:
        Tuple of (is_healthy, message)
    """
    if driver is None:
        return False, "Neo4j driver not initialized"
    
    try:
        database = config.NEO4J_DATABASE or "neo4j"
        with driver.session(database=database) as session:
            session.run("RETURN 1")
        return True, "Connection successful"
    except Exception as e:
        return False, f"Connection failed: {str(e)}"


def close_neo4j() -> None:
    """Close Neo4j database connection."""
    global driver
    if driver:
        driver.close()
        driver = None

