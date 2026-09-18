from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from services.patient_service import PatientService
from schemas.patient_schema import patient_schema
from utils.role_required import role_required
from utils.response import success_response, error_response


class PatientResource(Resource):

    # Get all patients
    @role_required("admin", "doctor", "receptionist")
    def get(self):
        """
        Get all patients
        ---
        tags:
          - Patients
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
            description: Number of patients per page

          - name: search
            in: query
            type: string
            required: false
            description: Search patients by name, phone, or email

          - name: gender
            in: query
            type: string
            required: false
            description: Filter patients by gender

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
            enum:
              - asc
              - desc
            default: asc
            description: Sorting order

        responses:
          200:
            description: List of patients
          401:
            description: Missing or invalid access token
          403:
            description: Access denied
        """
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        search = request.args.get("search")
        gender = request.args.get("gender")
        sort_by = request.args.get("sort_by", "id")
        order = request.args.get("order", "asc")

        result = PatientService.get_patients(
            page=page,
            per_page=per_page,
            search=search,
            gender=gender,
            sort_by=sort_by,
            order=order
        )

        return success_response(
            message="Patients fetched successfully",
            data=result,
            status_code=200
        ) 
        
        
        
    # Create patient
    @role_required("admin", "receptionist")
    def post(self):
        """
        Create a new patient
        ---
        tags:
          - Patients
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
              properties:
                first_name:
                  type: string
                  example: Rahul
                last_name:
                  type: string
                  example: Sharma
                phone:
                  type: string
                  example: "9876543210"
                email:
                  type: string
                  example: "rahul@example.com"
                gender:
                  type: string
                  example: Male
        responses:
          201:
            description: Patient created successfully
          400:
            description: Validation failed
          401:
            description: Missing or invalid access token
          403:
            description: Access denied
        """

        data = request.get_json()

        if not data:
            return error_response(
                "Request body must contain JSON data",
                400
            )

        try:
            validated_data = patient_schema.load(data)

        except ValidationError as err:
            return error_response(
                "Validation failed",
                400,
                errors=err.messages
            )

        result = PatientService.create_patient(validated_data)

        if isinstance(result, tuple):
            return result

        return success_response(
            "Patient created successfully",
            result,
            201
        )

class PatientDetailResource(Resource):

    # Get patient details by ID
    @role_required("admin", "doctor")
    def get(self, patient_id):
        """
        Get patient details by ID
        ---
        tags:
          - Patients
        security:
          - BearerAuth: []
        parameters:
          - name: patient_id
            in: path
            type: integer
            required: true
            description: Patient ID
        responses:
          200:
            description: Patient details retrieved successfully
          404:
            description: Patient not found
          401:
            description: Missing or invalid access token
          403:
            description: Access denied
        """
            
        result = PatientService.get_patient(patient_id)

        if isinstance(result, tuple):
            data, status_code = result

            if status_code != 200:
                return data, status_code

            return success_response(
                "Patient retrieved successfully",
                data,
                status_code         
            )

        return success_response(
            "Patient retrieved successfully",
            result,
            200)
        
        
        
    # Update patient details by ID
    @role_required("admin", "doctor", "receptionist")
    def put(self, patient_id):
        """
        Update patient details by ID
        ---
        tags:
          - Patients
        security:
          - BearerAuth: []
        consumes:
          - application/json
        parameters:
          - name: patient_id
            in: path
            type: integer
            required: true
            description: Patient ID

          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                first_name:
                  type: string
                  example: Satyendra
                last_name:
                  type: string
                  example: Dwivedi
                phone:
                  type: string
                  example: "9876543210"
                email:
                  type: string
                  example: "satyendra@example.com"
                gender:
                  type: string
                  example: Male
        responses:
          200:
            description: Patient updated successfully
          400:
            description: Invalid request data
          404:
            description: Patient not found
          401:
            description: Missing or invalid access token
          403:
            description: Access denied
        """

        data = request.get_json()

        try:
            validated_data = patient_schema.load(
                data,
                partial=True
            )
        except ValidationError as e:
            return {
                "success": False,
                "message": "Validation error",
                "errors": e.messages
            }, 400

        result = PatientService.update_patient(
            patient_id,
            validated_data
        )

        if isinstance(result, tuple):
            response_data, status_code = result

            if status_code != 200:
                return response_data, status_code

            return success_response(
                "Patient updated successfully",
                response_data,
                status_code
            )

        return success_response(
            "Patient updated successfully",
            result,
            200
        )


    # Delete patient by ID
    @role_required("admin")
    def delete(self, patient_id):
        """
        Delete patient by ID
        ---
        tags:
          - Patients
        security:
          - BearerAuth: []
        parameters:
          - name: patient_id
            in: path
            type: integer
            required: true
            description: Patient ID
        responses:
          200:
            description: Patient deleted successfully
          404:
            description: Patient not found
          401:
            description: Missing or invalid access token
          403:
            description: Access denied
        """

        result = PatientService.delete_patient(patient_id)

        if isinstance(result, tuple):
            return result

        return success_response(
            "Patient deleted successfully",
            status_code=200
        )