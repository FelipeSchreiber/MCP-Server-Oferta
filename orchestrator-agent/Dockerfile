# Orchestrator Agent Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY orchestrator.py .
COPY config.py .
COPY memory.py .
COPY test_orchestrator_docker.py .
COPY test_docker_simple.py .

# Create non-root user
RUN useradd --create-home --shell /bin/bash orchestrator && \
    chown -R orchestrator:orchestrator /app

USER orchestrator

# Default command runs simple test
CMD ["python", "test_docker_simple.py"]
