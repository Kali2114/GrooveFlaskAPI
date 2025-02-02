"""
Error handling for app.
"""

from flask import Response, jsonify

from app import app, db

class ErrorResponse:

    def __init__(self, message: str, http_status: int):
        self.payload = {
            "success": False,
            "message": message
        }
        self.http_status = http_status

    def to_response(self) -> Response:
        response = jsonify(self.payload)
        response.status_code = self.http_status
        return response


@app.errorhandler(404)
def not_found_error(error):
    """404 error."""
    return ErrorResponse(error.description, 404).to_response()


@app.errorhandler(400)
def bad_request_error(error):
    """400 error."""
    message = error.data.get("messages  ", {}).get("json", {})
    return ErrorResponse(message, 400).to_response()


@app.errorhandler(415)
def unsupported_media_type_error(error):
    return ErrorResponse(error.descrition, 415).to_response()


@app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return ErrorResponse(error.descrition, 500).to_response()