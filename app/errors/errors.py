"""
Error handling for app.
"""

from flask import Response, jsonify

from app import db
from app.errors import errors_bp


class ErrorResponse:

    def __init__(self, message: str, http_status: int):
        self.payload = {"success": False, "message": message}
        self.http_status = http_status

    def to_response(self) -> Response:
        response = jsonify(self.payload)
        response.status_code = self.http_status
        return response


@errors_bp.app_errorhandler(404)
def not_found_error(error):
    """404 error."""
    return ErrorResponse(error.description, 404).to_response()


@errors_bp.app_errorhandler(400)
def bad_request_error(error):
    """400 error."""
    message = error.data.get("messages", {}).get("json", {})
    return ErrorResponse(message, 400).to_response()


@errors_bp.app_errorhandler(401)
def unauthorized_error(error):
    """401 error."""
    return ErrorResponse(error.description, 401).to_response()


@errors_bp.app_errorhandler(415)
def unsupported_media_type_error(error):
    return ErrorResponse(error.description, 415).to_response()


@errors_bp.app_errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return ErrorResponse(error.description, 500).to_response()


@errors_bp.app_errorhandler(409)
def conflict_error(error):
    return ErrorResponse(error.description, 409).to_response()
