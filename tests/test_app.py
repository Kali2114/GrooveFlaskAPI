"""
Tests for app.
"""

from flask import Flask


def test_app(app):
    assert isinstance(app, Flask) is True
    assert app.config["TESTING"] is True
    assert app.config["DEBUG"] is True