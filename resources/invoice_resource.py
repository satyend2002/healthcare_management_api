from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from schemas.invoice_schema import invoice_schema
from services.invoice_service import InvoiceService


class InvoiceListResource(Resource):

    def get(self):
        invoices = InvoiceService.get_all()

        return (
            invoice_schema.dump(
                invoices,
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
            validated_data = invoice_schema.load(data)

        except ValidationError as err:
            return {
                "message": "Validation failed",
                "errors": err.messages
            }, 400

        try:
            result = InvoiceService.create(
                validated_data
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 400

        return (
            invoice_schema.dump(result),
            201
        )


class InvoiceResource(Resource):

    def get(self, invoice_id):
        try:
            invoice = InvoiceService.get_by_id(
                invoice_id
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return (
            invoice_schema.dump(invoice),
            200
        )

    def put(self, invoice_id):
        data = request.get_json()

        if not data:
            return {
                "message": "Request body must contain JSON data"
            }, 400

        try:
            validated_data = invoice_schema.load(
                data,
                partial=True
            )

        except ValidationError as err:
            return {
                "message": "Validation failed",
                "errors": err.messages
            }, 400

        try:
            result = InvoiceService.update(
                invoice_id,
                validated_data
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return {
            "message": "Invoice updated successfully",
            "invoice": invoice_schema.dump(result)
        }, 200

    def delete(self, invoice_id):
        try:
            InvoiceService.delete(
                invoice_id
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return {
            "message": "Invoice deleted successfully"
        }, 200


class InvoicesByPatientResource(Resource):

    def get(self, patient_id):
        try:
            invoices = InvoiceService.get_by_patient_id(patient_id)

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return (
            invoice_schema.dump(
                invoices,
                many=True
            ),
            200
        )