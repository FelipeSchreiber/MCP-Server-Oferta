from __future__ import annotations

from utils.formatters import format_success_response, format_error_response, format_mcp_response


def test_format_mcp_response_basic():
    result = format_mcp_response(
        title="Test Title",
        content={"foo": "bar"},
        agent_summary="did something",
    )
    assert "##### Test Title" in result
    assert "**Foo:** bar" in result
    assert "AGENT SUMMARY: did something" in result


def test_format_success_response_includes_action_and_summary():
    result = format_success_response("Greeting", {"name": "Alice"})
    assert "Greeting Completed" in result
    assert "**Name:** Alice" in result
    assert "AGENT SUMMARY" in result


def test_format_error_response_includes_context():
    result = format_error_response("boom", context="testing")
    assert "##### ❌ Error" in result
    assert "**Context:** testing" in result
    assert "**Error:** boom" in result
