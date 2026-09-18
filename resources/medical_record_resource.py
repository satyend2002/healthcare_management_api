from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from schemas.medical_record_schema import medical_record_schema
from services.medical_record_service import MedicalRecordService


class MedicalRecordListResource(Resource):

    def get(self):
        """
    Get all medical records
    ---
    tags:
      - Medical Records
    responses:
      200:
        description: List of medical records
    """
        medical_records = MedicalRecordService.get_all()

        return (
            medical_record_schema.dump(
                medical_records,
                many=True
            ),
            200
        )

    def post(self):
        """
    Create a medical record
    ---
    tags:
      - Medical Records
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            patient_id:
              type: integer
              example: 1
            doctor_id:
              type: integer
              example: 1
            diagnosis:
              type: string
              example: Fever
            notes:
              type: string
              example: Patient advised rest and medication
    responses:
      201:
        description: Medical record created successfully
      400:
        description: Invalid request data
    """
        data = request.get_json()

        if not data:
            return {
                "message": "Request body must contain JSON data"
            }, 400

        try:
            validated_data = medical_record_schema.load(data)

        except ValidationError as err:
            return {
                "message": "Validation failed",
                "errors": err.messages
            }, 400

        try:
            result = MedicalRecordService.create(
                validated_data
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return (
            medical_record_schema.dump(result),
            201
        )


class MedicalRecordResource(Resource):

    def get(self, medical_record_id):
        """
    Get a medical record by ID
    ---
    tags:
      - Medical Records
    parameters:
      - in: path
        name: record_id
        type: integer
        required: true
    responses:
      200:
        description: Medical record details
      404:
        description: Medical record not found
    """
        try:
            medical_record = MedicalRecordService.get_by_id(
                medical_record_id
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return (
            medical_record_schema.dump(
                medical_record
            ),
            200
        )

    def put(self, medical_record_id):
        """
    Update a medical record
    ---
    tags:
      - Medical Records
    parameters:
      - in: path
        name: record_id
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            diagnosis:
              type: string
              example: Updated diagnosis
            notes:
              type: string
              example: Updated medical notes
    responses:
      200:
        description: Medical record updated successfully
      404:
        description: Medical record not found
    """
        data = request.get_json()

        if not data:
            return {
                "message": "Request body must contain JSON data"
            }, 400

        try:
            validated_data = medical_record_schema.load(
                data,
                partial=True
            )

        except ValidationError as err:
            return {
                "message": "Validation failed",
                "errors": err.messages
            }, 400

        try:
            result = MedicalRecordService.update(
                medical_record_id,
                validated_data
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return {
            "message": "Medical record updated successfully",
            "medical_record": medical_record_schema.dump(
                result
            )
        }, 200

    def delete(self, medical_record_id):
        """
    Delete a medical record
    ---
    tags:
      - Medical Records
    parameters:
      - in: path
        name: record_id
        type: integer
        required: true
    responses:
      200:
        description: Medical record deleted successfully
      404:
        description: Medical record not found
    """
        try:
            MedicalRecordService.delete(
                medical_record_id
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return {
            "message": "Medical record deleted successfully"
        }, 200


class MedicalRecordsByPatientResource(Resource):

    def get(self, patient_id):
        try:
            medical_records = (
                MedicalRecordService.get_by_patient_id(
                    patient_id
                )
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return (
            medical_record_schema.dump(
                medical_records,
                many=True
            ),
            200
        )