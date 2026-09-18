from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required

from schemas.prescription_schema import prescription_schema
from services.prescription_service import PrescriptionService


class PrescriptionListResource(Resource):
    @jwt_required()
    def get(self):
        """
    Get a paginated list of prescriptions
    ---
    tags:
      - Prescriptions
    security:
      - BearerAuth: []
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
      - name: per_page
        in: query
        type: integer
        default: 10
    responses:
      200:
        description: Prescriptions retrieved successfully
      400:
        description: Invalid pagination parameters
      401:
        description: Missing or invalid access token
      403:
        description: Access denied
    """
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)

        result = PrescriptionService.get_all(
            page=page,
            per_page=per_page
        )

        return {
            "message": "Prescriptions retrieved successfully",
            "data": prescription_schema.dump(
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

    def post(self):
        """
    Create a new prescription
    ---
    tags:
      - Prescriptions
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
            - patient_id
            - doctor_id
            - appointment_id
          properties:
            patient_id:
              type: integer
              example: 1
            doctor_id:
              type: integer
              example: 1
            appointment_id:
              type: integer
              example: 1
            notes:
              type: string
              example: Take medicines after meals
    responses:
      201:
        description: Prescription created successfully
      400:
        description: Validation failed
      404:
        description: Related entity not found
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
            validated_data = prescription_schema.load(data)

        except ValidationError as err:
            return {
                "message": "Validation failed",
                "errors": err.messages
            }, 400

        try:
            result = PrescriptionService.create(
                validated_data
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return prescription_schema.dump(result), 201


class PrescriptionResource(Resource):

    def get(self, prescription_id):
        """
    Get prescription details by ID
    ---
    tags:
      - Prescriptions
    security:
      - BearerAuth: []
    parameters:
      - name: prescription_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Prescription details retrieved successfully
      404:
        description: Prescription not found
      401:
        description: Missing or invalid access token
      403:
        description: Access denied
    """

        try:
            prescription = PrescriptionService.get_by_id(
                prescription_id
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return prescription_schema.dump(
            prescription
        ), 200

    def put(self, prescription_id):
        """
    Update prescription details by ID
    ---
    tags:
      - Prescriptions
    security:
      - BearerAuth: []
    consumes:
      - application/json
    parameters:
      - name: prescription_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            notes:
              type: string
              example: Continue medication for five days
    responses:
      200:
        description: Prescription updated successfully
      400:
        description: Validation failed
      404:
        description: Prescription not found
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
            validated_data = prescription_schema.load(
                data,
                partial=True
            )

        except ValidationError as err:
            return {
                "message": "Validation failed",
                "errors": err.messages
            }, 400

        try:
            result = PrescriptionService.update(
                prescription_id,
                validated_data
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return {
            "message": "Prescription updated successfully",
            "prescription": prescription_schema.dump(result)
        }, 200

    def delete(self, prescription_id):
        """
    Delete prescription by ID
    ---
    tags:
      - Prescriptions
    security:
      - BearerAuth: []
    parameters:
      - name: prescription_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Prescription deleted successfully
      404:
        description: Prescription not found
      401:
        description: Missing or invalid access token
      403:
        description: Access denied
    """
        try:
            PrescriptionService.delete(
                prescription_id
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return {
            "message": "Prescription deleted successfully"
        }, 200