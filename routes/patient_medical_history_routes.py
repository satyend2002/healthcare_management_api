from flask import Blueprint
from flask_restful import Api

from resources.patient_medical_history_resource import (
    PatientMedicalHistoryListResource,
    PatientMedicalHistoryResource,
    PatientMedicalHistoryByPatientResource
)


patient_medical_history_bp = Blueprint(
    "patient_medical_history",
    __name__,
    url_prefix="/api/v1/patient-medical-history"
)

patient_medical_history_api = Api(
    patient_medical_history_bp
)


patient_medical_history_api.add_resource(
    PatientMedicalHistoryListResource,
    ""
)

patient_medical_history_api.add_resource(
    PatientMedicalHistoryResource,
    "/<int:history_id>"
)

patient_medical_history_api.add_resource(
    PatientMedicalHistoryByPatientResource,
    "/patient/<int:patient_id>"
)