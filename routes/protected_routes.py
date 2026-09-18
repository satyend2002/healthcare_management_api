from flask import Blueprint
from flask_restful import Api

from resources.protected_resource import ProtectedResource


protected_bp = Blueprint(
    "protected",
    __name__,
    url_prefix="/api/v1/protected"
)

protected_api = Api(protected_bp)

protected_api.add_resource(
    ProtectedResource,
    ""
)