"""Blueprints for app."""

from flask import Blueprint


artists_bp = Blueprint("artists", __name__)

from app.artists import artists
