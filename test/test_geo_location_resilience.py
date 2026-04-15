"""Regression tests for resilient reverse geocoding."""

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "climsight"))

from geo_functions import get_location


class _FakeResponse:
    def __init__(self, *, status_code=200, text="", headers=None):
        self.status_code = status_code
        self.text = text
        self.headers = headers or {}

    def json(self):
        return json.loads(self.text)


def test_get_location_returns_none_for_non_json_response(monkeypatch):
    get_location.cache_clear()
    monkeypatch.setattr(
        "geo_functions.requests.get",
        lambda *args, **kwargs: _FakeResponse(
            text="<html>rate limited</html>",
            status_code=200,
            headers={"Content-Type": "text/html"},
        ),
    )

    location = get_location(12.34, 56.78)

    assert location is None


def test_get_location_returns_none_for_http_error(monkeypatch):
    get_location.cache_clear()
    monkeypatch.setattr(
        "geo_functions.requests.get",
        lambda *args, **kwargs: _FakeResponse(
            text="Too Many Requests",
            status_code=429,
            headers={"Content-Type": "text/plain"},
        ),
    )

    location = get_location(12.35, 56.79)

    assert location is None
