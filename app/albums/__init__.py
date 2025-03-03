"""Blueprints for app."""

from flask import Blueprint


albums_bp = Blueprint("albums", __name__)

from app.albums import albums
