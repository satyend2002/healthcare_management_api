from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from services.doctor_service import DoctorService
from schemas.doctor_schema import doctor_schema
from utils.role_required import role_required


class DoctorResource(Resource):

    # Create doctor
    def post(self):
        """
    Create a new doctor
    ---
    tags:
      - Doctors
    security:
      - BearerAuth: []
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - first_name
            - last_name
            - specialization
            - department_id
          properties:
            first_name:
              type: string
              example: Amit
            last_name:
              type: string
              example: Sharma
            phone:
              type: string
              example: "9876543210"
            email:
              type: string
              example: amit@example.com
            specialization:
              type: string
              example: Cardiologist
            department_id:
              type: integer
              example: 1
    responses:
      201:
        description: Doctor created successfully
      400:
        description: Validation failed
      401:
        description: Missing or invalid access token
      403:
        description: Access denied
    """

        data = request.get_json()

        if not data:
            return {
                "message": "Request body must contain JSON data"
            }, 400

        try:
            validated_data = doctor_schema.load(data)

        except ValidationError as err:
            return {
                "message": "Validation failed",
                "errors": err.messages
            }, 400

        result = DoctorService.create_doctor(validated_data)

        if isinstance(result, tuple):
            return result

        return doctor_schema.dump(result), 201


    # Get all doctors .................
    @role_required("admin", "doctor", "receptionist")
    def get(self):
        """
    Get a paginated list of doctors
    ---
    tags:
      - Doctors
    security:
      - BearerAuth: []
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        default: 1
        description: Page number
      - name: per_page
        in: query
        type: integer
        required: false
        default: 10
        description: Number of doctors per page
      - name: search
        in: query
        type: string
        required: false
        description: Search by doctor name, phone, or email
      - name: specialization
        in: query
        type: string
        required: false
        description: Filter by specialization
      - name: sort_by
        in: query
        type: string
        required: false
        default: id
        description: Field used for sorting
      - name: order
        in: query
        type: string
        required: false
        default: asc
        enum:
          - asc
          - desc
        description: Sorting order
    responses:
      200:
        description: Doctors retrieved successfully
      400:
        description: Invalid pagination parameters
      401:
        description: Missing or invalid access token
      403:
        description: Access denied
    """
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)

        search = request.args.get(
            "search",
            default="",
            type=str
        ).strip()

        specialization = request.args.get(
            "specialization",
            default="",
            type=str
        ).strip()

        sort_by = request.args.get(
            "sort_by",
            default="id",
            type=str
        ).strip()

        order = request.args.get(
            "order",
            default="asc",
            type=str
        ).strip().lower()

        result = DoctorService.get_all_doctors(
            page=page,
            per_page=per_page,
            search=search,
            specialization=specialization,
            sort_by=sort_by,
            order=order
        )

        return {
            "message": "Doctors retrieved successfully",
            "data": doctor_schema.dump(
                result.items,
                many=True
            ),
            "pagination": {
                "page": result.page,
                "per_page": result.per_page,
                "total": result.total,
                "pages": result.pages,
                "has_next": result.has_next,
                "has_prev": result.has_prev
            }
        }, 200

class DoctorDetailResource(Resource):

    # Get doctor by ID
    def get(self, doctor_id):
        """
    Get doctor details by ID
    ---
    tags:
      - Doctors
    security:
      - BearerAuth: []
    parameters:
      - name: doctor_id
        in: path
        type: integer
        required: true
        description: Doctor ID
    responses:
      200:
        description: Doctor details retrieved successfully
      404:
        description: Doctor not found
      401:
        description: Missing or invalid access token
      403:
        description: Access denied
    """

        doctor = DoctorService.get_doctor(doctor_id)

        if not doctor:
            return {
                "message": "Doctor not found"
            }, 404

        return doctor_schema.dump(doctor), 200


    # Update doctor ..................
    def put(self, doctor_id):
        """
    Update doctor details by ID
    ---
    tags:
      - Doctors
    security:
      - BearerAuth: []
    consumes:
      - application/json
    parameters:
      - name: doctor_id
        in: path
        type: integer
        required: true
        description: Doctor ID
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            first_name:
              type: string
              example: Amit
            last_name:
              type: string
              example: Sharma
            phone:
              type: string
              example: "9876543210"
            email:
              type: string
              example: amit@example.com
            specialization:
              type: string
              example: Cardiologist
            department_id:
              type: integer
              example: 1
    responses:
      200:
        description: Doctor updated successfully
      400:
        description: Validation failed
      404:
        description: Doctor not found
      401:
        description: Missing or invalid access token
      403:
        description: Access denied
    """

        data = request.get_json()

        if not data:
            return {
                "message": "Request body must contain JSON data"
            }, 400

        try:
            validated_data = doctor_schema.load(data)

        except ValidationError as err:
            return {
                "message": "Validation failed",
                "errors": err.messages
            }, 400

        result = DoctorService.update_doctor(
            doctor_id,
            validated_data
        )

        if isinstance(result, tuple):
            return result

        return {
            "message": "Doctor updated successfully",
            "doctor": doctor_schema.dump(result)
        }, 200


    # Delete doctor  ..............
    def delete(self, doctor_id):
        """
    Delete doctor by ID
    ---
    tags:
      - Doctors
    security:
      - BearerAuth: []
    parameters:
      - name: doctor_id
        in: path
        type: integer
        required: true
        description: Doctor ID
    responses:
      200:
        description: Doctor deleted successfully
      404:
        description: Doctor not found
      401:
        description: Missing or invalid access token
      403:
        description: Access denied
    """

        result = DoctorService.delete_doctor(doctor_id)

        return result