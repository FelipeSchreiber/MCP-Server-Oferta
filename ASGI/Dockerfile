FROM python:3.11-slim

WORKDIR /app

# Install dependencies (pin versions)
RUN pip install --no-cache-dir fastmcp==0.4.1 starlette==0.45.2 uvicorn==0.34.0

# Copy server file
COPY fastmcp_server_template.py .

# Expose port
EXPOSE 8000

# Run the ASGI server with uvicorn
CMD ["uvicorn", "fastmcp_server_template:app", "--host", "0.0.0.0", "--port", "8000"]
