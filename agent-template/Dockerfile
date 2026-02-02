# Agent Template Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY agent.py .
COPY mcp_client.py .
COPY config.py .
COPY memory.py .
COPY test_agent_docker.py .
COPY test_docker_simple.py .

# Create non-root user
RUN useradd --create-home --shell /bin/bash agent && \
    chown -R agent:agent /app

USER agent

# Default command runs simple test
CMD ["python", "test_docker_simple.py"]
