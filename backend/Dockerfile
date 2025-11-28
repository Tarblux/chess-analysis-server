# Use Python 3.13 slim image as base
FROM python:3.13-slim

# Install curl for healthchecks
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Copy application source code
COPY src/ ./src/

# Expose the port the app runs on
EXPOSE 5150

# Set environment variable to use uv's Python
ENV PATH="/app/.venv/bin:$PATH"

# Run the Flask application with Gunicorn ( Apparently the default flask server is trash and gunicorn is better...idk lol)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5150", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "src.main:app"]
