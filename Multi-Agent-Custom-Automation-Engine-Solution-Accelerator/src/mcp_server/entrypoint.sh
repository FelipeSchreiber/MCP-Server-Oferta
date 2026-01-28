#!/bin/bash
set -e

# Check if OpenTelemetry instrumentation should be enabled
if [ "$ENABLE_OTEL" = "true" ]; then
  echo "🔭 Starting with OpenTelemetry instrumentation..."
  exec opentelemetry-instrument \
    --service_name "${OTEL_SERVICE_NAME:-mcp-server}" \
    --exporter_otlp_endpoint "${OTEL_EXPORTER_OTLP_ENDPOINT:-http://localhost:4317}" \
    python mcp_server.py --transport streamable-http --host 0.0.0.0 --port 9000
else
  echo "🚀 Starting without OpenTelemetry..."
  exec python mcp_server.py --transport streamable-http --host 0.0.0.0 --port 9000
fi
