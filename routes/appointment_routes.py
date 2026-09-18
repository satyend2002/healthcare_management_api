from flask import Blueprint
from flask_restful import Api

from resources.appointment_resource import (
    AppointmentListResource,
    AppointmentResource 
)


appointment_bp = Blueprint(
    "appointment",
    __name__,
    url_prefix="/api/v1/appointments" 
)

appointment_api = Api(appointment_bp)

appointment_api.add_resource(
    AppointmentListResource,
    ""
)

appointment_api.add_resource(
    AppointmentResource,
    "/<int:appointment_id>"
)