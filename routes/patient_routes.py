
from flask import Blueprint  
from flask_restful import Api 

from resources.patient_resource import PatientDetailResource, PatientResource

# Create a Blueprint for patient routes ............
patient_bp = Blueprint(
    "patient",
    __name__,
    url_prefix="/api/v1/patients"
)
                                                                                                                     
patient_api = Api(patient_bp) # Initialize Flask-RESTful API for the patient blueprint ....
# here we are saying that all the patient routes are defined in this patient blueprint will be prefixed with /api/v1/patients

patient_api.add_resource(PatientResource, "")       
patient_api.add_resource(PatientDetailResource, "/<int:patient_id>")