from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from schemas.patient_medical_history_schema import (
    patient_medical_history_schema
)

from services.patient_medical_history_service import (
    PatientMedicalHistoryService
)


class PatientMedicalHistoryListResource(Resource):

    def get(self):
        histories = (
            PatientMedicalHistoryService.get_all()
        )

        return (
            patient_medical_history_schema.dump(
                histories,
                many=True
            ),
            200
        )

    def post(self):
        data = request.get_json()

        if not data:
            return {
                "message": "Request body must contain JSON data"
            }, 400

        try:
            validated_data = (
                patient_medical_history_schema.load(data)
            )

        except ValidationError as err:
            return {
                "message": "Validation failed",
                "errors": err.messages
            }, 400

        try:
            result = PatientMedicalHistoryService.create(
                validated_data
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return (
            patient_medical_history_schema.dump(result),
            201
        )


class PatientMedicalHistoryResource(Resource):

    def get(self, history_id):
        try:
            history = (
                PatientMedicalHistoryService.get_by_id(
                    history_id
                )
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return (
            patient_medical_history_schema.dump(
                history
            ),
            200
        )

    def put(self, history_id):
        data = request.get_json()

        if not data:
            return {
                "message": "Request body must contain JSON data"
            }, 400

        try:
            validated_data = (
                patient_medical_history_schema.load(
                    data,
                    partial=True
                )
            )

        except ValidationError as err:
            return {
                "message": "Validation failed",
                "errors": err.messages
            }, 400

        try:
            result = (
                PatientMedicalHistoryService.update(
                    history_id,
                    validated_data
                )
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return {
            "message": "Patient medical history updated successfully",
            "history": patient_medical_history_schema.dump(
                result
            )
        }, 200

    def delete(self, history_id):
        try:
            PatientMedicalHistoryService.delete(
                history_id
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return {
            "message": "Patient medical history deleted successfully"
        }, 200


class PatientMedicalHistoryByPatientResource(Resource):

    def get(self, patient_id):
        try:
            histories = (
                PatientMedicalHistoryService
                .get_by_patient_id(patient_id)
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return (
            patient_medical_history_schema.dump(
                histories,
                many=True
            ),
            200
        )