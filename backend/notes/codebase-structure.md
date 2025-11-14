# Codebase Structure

```
/backend
├── .env                  # Environment variables and secrets
├── .gitignore
├── docker-compose.yml    # Defines and runs all services (API, workers, DBs)
├── Dockerfile            # Builds the Python application image
├── pyproject.toml        # Project dependencies for `uv`
├── README.md
└── /src                  # Main source code for the application
    ├── main.py           # Application entry point (creates Flask app)
    ├── config.py         # Configuration classes (Dev, Prod, etc.)
    ├── /api              # Flask-related components
    │   ├── __init__.py
    │   ├── routes.py     # API endpoints (e.g., @app.route('/games'))
    │   └── schemas.py    # Data serialization/validation (Pydantic/Marshmallow)
    ├── /models           # SQLAlchemy and Neo4j models
    │   ├── __init__.py
    │   ├── postgres_models.py # User, Game, Analysis tables
    │   └── graph_models.py    # Opening Tree nodes/relationships
    ├── /services         # Core business logic
    │   ├── __init__.py
    │   ├── game_analysis_service.py
    │   └── aggregation_service.py
    ├── /workers           # Celery task definitions
    │   ├── __init__.py
    │   ├── ingestion.py  # Tasks for the Game Ingestion Worker
    │   ├── analysis.py   # Tasks for the Game Analysis Worker
    │   └── aggregation.py# Tasks for the Aggregation Worker
    └── /core             # Shared instances (db, celery)
        ├── __init__.py
        ├── database.py   # Database connection and session management
        ├── celery_app.py # Celery application instance setup
        └── extensions.py # SQLAlchemy, etc., instances
```

---

## Breakdown of Key Directories

### 📂 `src/`

This is the main Python package for your project. The `main.py` file contains the application factory pattern (`create_app()`) which is a Flask best practice that helps avoid circular imports, especially when integrating extensions like SQLAlchemy and Celery.

### 📂 `src/api/`

This directory holds everything related to your web-facing API.

* **`routes.py`** : Defines all your API endpoints. Each route function should be lightweight, responsible only for handling the HTTP request and calling the appropriate service to do the actual work.
* **`schemas.py`** : (Highly Recommended) Defines the expected structure of your API's inputs and outputs. This is great for data validation and consistent responses.

### 📂 `src/services/`

This is the **brain** of your application and directly maps to the "Services" layer in your diagram. All complex business logic lives here. For example, `game_analysis_service.py` would contain the functions to calculate game accuracy or find blunders, which can be called by both the API (for a single request) or a Celery task (for a background job).

### 📂 `src/workers/`

This is where you define all your Celery tasks. Each file corresponds to a worker type from your diagram. For example, `ingestion.py` will have a task like `@celery.task def fetch_games_from_chess_com()`. These tasks will import and use your services to perform their work.

### 📂 `src/models/`

This directory is for your data definitions. You can split your SQLAlchemy (PostgreSQL) models and your Neo4j models into separate files to keep things clean as they will use different clients/libraries to interact with the databases.

### 📂 `src/core/`

This directory contains shared infrastructure components:
* **`database.py`** : Database connection setup, session management, and initialization
* **`celery_app.py`** : Celery application instance and configuration
* **`extensions.py`** : Shared extension instances (SQLAlchemy, etc.)

---

## Core Files at the Root

* **`docker-compose.yml`** : This is a crucial file. It will define not just your Python application but *all* the services it depends on: the **Flask API**, one or more **Celery workers**, **PostgreSQL**, **RabbitMQ**, and **Neo4j**. This allows you to spin up your entire development environment with a single `docker-compose up` command.
* **`pyproject.toml`** : This is the modern standard for managing Python project metadata and dependencies. `uv` will use this file to install everything needed for your project.
* **`.env`** : Stores configuration that changes between environments or contains secrets, such as your `DATABASE_URL`, `RABBITMQ_URL`, and [Chess.com](http://Chess.com) API keys.
