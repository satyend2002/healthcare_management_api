from flask import jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        response = {
            "success": False,
            "message": error.description,
            "error": error.name,
            "status_code": error.code
        }

        return jsonify(response), error.code

    @app.errorhandler(Exception)
    def handle_general_exception(error):
        app.logger.exception("Unhandled exception occurred")

        response = {
            "success": False,
            "message": "An internal server error occurred",
            "error": "Internal Server Error",
            "status_code": 500
        }

        return jsonify(response), 500