# Use Python 3.11 slim as base image
FROM python:3.11-slim AS base
WORKDIR /app

# Builder stage with uv for dependency management
FROM base AS builder
COPY --from=ghcr.io/astral-sh/uv:0.6.3 /uv /uvx /bin/

# Copy all files
COPY . /app

# Install all dependencies
RUN uv sync --no-dev

# Final stage
FROM base
WORKDIR /app

# Copy installed dependencies and application
COPY --from=builder /app /app
COPY --from=builder /bin/uv /bin/uv

# Create non-root user
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app

# Switch to non-root user
USER app

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"

# Expose port
EXPOSE 9000

# Run the server
CMD ["uv", "run", "python", "mcp_server.py", "--transport", "streamable-http", "--host", "0.0.0.0", "--port", "9000"]
