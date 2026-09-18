from flask import Blueprint
from flask_restful import Api

from resources.user_resource import (
    UserRegistrationResource,
    UserListResource,
    AdminCreateUserResource
)


user_bp = Blueprint(
    "user",
    __name__,
    url_prefix="/api/v1/users"
)

user_api = Api(user_bp)


user_api.add_resource(
    UserRegistrationResource,
    "/register"
)

user_api.add_resource(
    UserListResource,
    ""
)

user_api.add_resource(
    AdminCreateUserResource,
    "/admin-create"
)