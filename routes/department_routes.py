from flask import Blueprint
from flask_restful import Api

from resources.department import (
    DepartmentResource,
    DepartmentDetailResource
)


department_bp = Blueprint(
    "department",
    __name__,
    url_prefix="/api/v1/departments"
)

department_api = Api(department_bp) # Initialize Flask-RESTful API for the department blueprint ... 

department_api.add_resource(DepartmentResource,"") 

department_api.add_resource(DepartmentDetailResource, "/<int:department_id>")