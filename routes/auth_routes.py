from flask import Blueprint
from flask_restful import Api


from resources.auth_resource import (
    LoginResource,
    RefreshTokenResource,
    LogoutResource,
    LogoutAccessTokenResource 
) 

    

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/v1/auth"
)

auth_api = Api(auth_bp)

auth_api.add_resource(
    LoginResource,
    "/login"
)

auth_api.add_resource(
    RefreshTokenResource,
    "/refresh"
)

auth_api.add_resource(
    LogoutResource, 
    "/logout"
    )

auth_api.add_resource(
    LogoutAccessTokenResource,
    "/logout-access"
) 