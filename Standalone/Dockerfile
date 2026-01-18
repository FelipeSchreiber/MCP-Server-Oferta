FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir fastmcp

# Copy the server file
COPY fastmcp_server_template.py .

# Expose the port the server runs on
EXPOSE 8000

# Run the FastMCP server
CMD ["python", "fastmcp_server_template.py"]
