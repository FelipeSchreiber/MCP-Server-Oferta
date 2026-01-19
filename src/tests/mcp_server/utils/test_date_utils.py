from __future__ import annotations

from utils.date_utils import format_date_for_user, get_current_timestamp, format_timestamp_for_display


def test_format_date_for_user_parses_common_formats():
    assert "January" in format_date_for_user("2024-01-18")
    assert "January" in format_date_for_user("2024-01-18 10:30:00")
    assert "January" in format_date_for_user("01/18/2024")


def test_format_date_for_user_falls_back_on_invalid():
    assert format_date_for_user("not-a-date") == "not-a-date"


def test_get_current_timestamp_returns_isoformat():
    ts = get_current_timestamp()
    assert "T" in ts
    assert ts.endswith("+00:00") or "Z" in ts


def test_format_timestamp_for_display_handles_none_and_invalid():
    formatted = format_timestamp_for_display()
    assert "UTC" in formatted
    assert format_timestamp_for_display("invalid") == "invalid"
