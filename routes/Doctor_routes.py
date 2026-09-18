from flask import Blueprint
from flask_restful import Api

from resources.doctor_resource import (
    DoctorResource,
    DoctorDetailResource
)


doctor_bp = Blueprint(
    "doctor",
    __name__,
    url_prefix="/api/v1/doctors"
)

doctor_api = Api(doctor_bp)
doctor_api.add_resource(DoctorResource,"")
doctor_api.add_resource(DoctorDetailResource,"/<int:doctor_id>")  

