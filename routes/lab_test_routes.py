from flask import Blueprint
from flask_restful import Api

from resources.lab_test_resource import (
    LabTestListResource,
    LabTestResource
)


lab_test_bp = Blueprint(
    "lab_test",
    __name__,
    url_prefix="/api/v1/lab-tests"
)

lab_test_api = Api(lab_test_bp)

lab_test_api.add_resource(
    LabTestListResource,
    ""
)

lab_test_api.add_resource(
    LabTestResource,
    "/<int:lab_test_id>"
)