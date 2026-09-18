from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from services.department_service import DepartmentService 
from schemas.department_schema import department_schema 
from utils.role_required import role_required


class DepartmentResource(Resource):

    # Create department
    def post(self):
        """
    Create a new department
    ---
    tags:
      - Departments
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: Cardiology
            description:
              type: string
              example: Department for heart-related treatment
    responses:
      201:
        description: Department created successfully
      400:
        description: Invalid request data
    """
        
        data = request.get_json()

        if not data:
            return {
                "message": "Request body must contain JSON data"
            }, 400

        try:
            validated_data = department_schema.load(data)

        except ValidationError as err:
            return {
                "message": "Validation failed",
                "errors": err.messages
            }, 400

        result = DepartmentService.create_department(validated_data)

        if isinstance(result, tuple):
            return result

        return department_schema.dump(result), 201


    # Get all departments ...........   
    @role_required("admin", "doctor", "receptionist")
    def get(self):
        """
    Get all departments
    ---
    tags:
      - Departments
    responses:
      200:
        description: List of departments
    """

        departments = DepartmentService.get_all_departments()

        return department_schema.dump(departments, many=True ), 200


class DepartmentDetailResource(Resource):

    # Get department by ID ............................
    def get(self, department_id):
        """
    Get a department by ID
    ---
    tags:
      - Departments
    parameters:
      - in: path
        name: department_id
        type: integer
        required: true
        description: Department ID
    responses:
      200:
        description: Department details
      404:
        description: Department not found
    """
        department = DepartmentService.get_department( department_id)

        if not department:
            return {
                "message": "Department not found"
            }, 404

        return department_schema.dump(department), 200


    # Update department ..................................
    def put(self, department_id):
        """
    Update a department
    ---
    tags:
      - Departments
    parameters:
      - in: path
        name: department_id
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: Cardiology
            description:
              type: string
              example: Updated department description
    responses:
      200:
        description: Department updated successfully
      404:
        description: Department not found
    """

        data = request.get_json() 

        if not data:
            return {
                "message": "Request body must contain JSON data"
            }, 400

        try:
            validated_data = department_schema.load(data)

        except ValidationError as err:
            return {
                "message": "Validation failed",
                "errors": err.messages
            }, 400

        result = DepartmentService.update_department(department_id,validated_data)

        if isinstance(result, tuple):
            return result

        return {
            "message": "Department updated successfully",
            "department": department_schema.dump(result)
        }, 200


    # Delete department .........................................
    def delete(self, department_id):
        """
    Delete a department
    ---
    tags:
      - Departments
    parameters:
      - in: path
        name: department_id
        type: integer
        required: true
    responses:
      200:
        description: Department deleted successfully
      404:
        description: Department not found
    """

        result = DepartmentService.delete_department(
            department_id
        )

        return result   