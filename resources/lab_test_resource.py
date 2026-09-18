from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from schemas.lab_test_schema import lab_test_schema
from services.lab_test_service import LabTestService


class LabTestListResource(Resource):

    def get(self):
        lab_tests = LabTestService.get_all()

        return lab_test_schema.dump(
            lab_tests,
            many=True
        ), 200

    def post(self):
        data = request.get_json()

        if not data:
            return {
                "message": "Request body must contain JSON data"
            }, 400

        try:
            validated_data = lab_test_schema.load(data)

        except ValidationError as err:
            return {
                "message": "Validation failed",
                "errors": err.messages
            }, 400

        try:
            result = LabTestService.create(validated_data)

        except ValueError as err:
            return {
                "message": str(err)
            }, 400

        return lab_test_schema.dump(result), 201


class LabTestResource(Resource):

    def get(self, lab_test_id):
        try:
            lab_test = LabTestService.get_by_id(lab_test_id)

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return lab_test_schema.dump(lab_test), 200

    def put(self, lab_test_id):
        data = request.get_json()

        if not data:
            return {
                "message": "Request body must contain JSON data"
            }, 400

        try:
            validated_data = lab_test_schema.load(
                data,
                partial=True
            )

        except ValidationError as err:
            return {
                "message": "Validation failed",
                "errors": err.messages
            }, 400

        try:
            result = LabTestService.update(
                lab_test_id,
                validated_data
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return {
            "message": "Laboratory test updated successfully",
            "lab_test": lab_test_schema.dump(result)
        }, 200

    def delete(self, lab_test_id):
        try:
            LabTestService.delete(lab_test_id)

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return {
            "message": "Laboratory test deleted successfully"
        }, 200