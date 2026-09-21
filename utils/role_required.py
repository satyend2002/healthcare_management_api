from functools import wraps

from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt
)

from flask_jwt_extended.exceptions import NoAuthorizationError


def role_required(*allowed_roles):

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            try:
                verify_jwt_in_request()
            except NoAuthorizationError:
                return {
                    "message": "Authorization token is required"
                }, 401

            claims = get_jwt()
            user_role = claims.get("role")

            if user_role not in allowed_roles:
                return {
                    "message": "Access denied. Insufficient permissions."
                }, 403

            return function(*args, **kwargs)

        return wrapper

    return decorator