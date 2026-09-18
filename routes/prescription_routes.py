from flask import Blueprint
from flask_restful import Api

from resources.prescription_resource import (
    PrescriptionListResource,
    PrescriptionResource
)


prescription_bp = Blueprint(
    "prescription",
    __name__,
    url_prefix="/api/v1/prescriptions"
)

prescription_api = Api(prescription_bp)


prescription_api.add_resource(
    PrescriptionListResource,
    ""
)


prescription_api.add_resource(
    PrescriptionResource,
    "/<int:prescription_id>"
)