"""OpenTelemetry tracing utilities for MCP tools."""

import functools
import os
from typing import Any, Callable

# Check if OTEL is enabled
OTEL_ENABLED = os.getenv("ENABLE_OTEL", "false").lower() == "true"

# Get tracer from OpenTelemetry if enabled
tracer = None
if OTEL_ENABLED:
    from opentelemetry import trace
    from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor

    HTTPXClientInstrumentor().instrument()
    tracer = trace.get_tracer(__name__)


def trace_span(span_name: str = None):
    """
    Simple decorator to trace any function with OpenTelemetry.

    Args:
        span_name: Optional custom span name. If not provided, uses function name.
    """
    def decorator(func: Callable) -> Callable:
        if not OTEL_ENABLED or not tracer:
            return func

        name = span_name or func.__name__

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            with tracer.start_as_current_span(name):
                return await func(*args, **kwargs)

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            with tracer.start_as_current_span(name):
                return func(*args, **kwargs)

        import asyncio
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    return decorator


def trace_tool_call(func: Callable) -> Callable:
    """
    Decorator to trace MCP tool calls with OpenTelemetry.

    Captures:
    - Tool name
    - Input arguments
    - Return value (truncated)
    - Execution time
    - Errors (if any)
    """
    if not OTEL_ENABLED or not tracer:
        return func

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs) -> Any:
        from opentelemetry.trace import Status, StatusCode

        tool_name = func.__name__

        with tracer.start_as_current_span(
            f"mcp.tool.{tool_name}",
            attributes={
                "tool.name": tool_name,
                "tool.args": str(args[1:] if args else ())[:200],
                "tool.kwargs": str(kwargs)[:200],
            }
        ) as span:
            try:
                result = await func(*args, **kwargs)
                span.set_attribute("tool.result", str(result)[:200])
                span.set_status(Status(StatusCode.OK))
                return result
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs) -> Any:
        from opentelemetry.trace import Status, StatusCode

        tool_name = func.__name__

        with tracer.start_as_current_span(
            f"mcp.tool.{tool_name}",
            attributes={
                "tool.name": tool_name,
                "tool.args": str(args[1:] if args else ())[:200],
                "tool.kwargs": str(kwargs)[:200],
            }
        ) as span:
            try:
                result = func(*args, **kwargs)
                span.set_attribute("tool.result", str(result)[:200])
                span.set_status(Status(StatusCode.OK))
                return result
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise

    import asyncio
    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper
