# Use Python 3.11 slim as base image
FROM python:3.11-slim
WORKDIR /app

# Install dependencies with pip
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application files
COPY . /app

# Create non-root user
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app

# Switch to non-root user
USER app

# Expose port
EXPOSE 9000

# Run the server
CMD ["python", "mcp_server.py", "--transport", "streamable-http", "--host", "0.0.0.0", "--port", "9000"]
