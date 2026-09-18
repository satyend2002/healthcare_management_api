from flask import Blueprint
from flask_restful import Api

from resources.medicine_resource import (
    MedicineListResource,
    MedicineResource
)

medicine_bp = Blueprint(
    "medicine",
    __name__,
    url_prefix="/api/v1/medicines"
)

medicine_api = Api(medicine_bp)


medicine_api.add_resource(
    MedicineListResource,
    ""
)

medicine_api.add_resource(
    MedicineResource,
    "/<int:medicine_id>"
) 