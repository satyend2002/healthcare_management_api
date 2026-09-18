from flask import Blueprint
from flask_restful import Api

from resources.prescription_item_resource import (
    PrescriptionItemListResource,
    PrescriptionItemResource,
    PrescriptionItemsByPrescriptionResource
)


prescription_item_bp = Blueprint(
    "prescription_item",
    __name__,
    url_prefix="/api/v1/prescription-items"
)

prescription_item_api = Api(prescription_item_bp)


prescription_item_api.add_resource(
    PrescriptionItemListResource,
    ""
)

prescription_item_api.add_resource(
    PrescriptionItemResource,
    "/<int:prescription_item_id>"
)


prescription_item_api.add_resource(
    PrescriptionItemsByPrescriptionResource,
    "/prescription/<int:prescription_id>"
)