from flask import Blueprint
from flask_restful import Api

from resources.medical_record_resource import (
    MedicalRecordListResource,
    MedicalRecordResource,
    MedicalRecordsByPatientResource
)


medical_record_bp = Blueprint(
    "medical_record",
    __name__,
    url_prefix="/api/v1/medical-records"
)

medical_record_api = Api(medical_record_bp)


medical_record_api.add_resource(
    MedicalRecordListResource,
    ""
)

medical_record_api.add_resource(
    MedicalRecordResource,
    "/<int:medical_record_id>"
)

medical_record_api.add_resource(
    MedicalRecordsByPatientResource,
    "/patient/<int:patient_id>"
)