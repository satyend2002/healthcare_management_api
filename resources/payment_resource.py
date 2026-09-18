from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from schemas.payment_schema import payment_schema
from services.payment_service import PaymentService


class PaymentListResource(Resource):

    def get(self):
        payments = PaymentService.get_all()
        return payment_schema.dump(payments, many=True), 200

    def post(self):
        data = request.get_json()

        if not data:
            return {
                "message": "Request body must contain JSON data"
            }, 400

        try:
            validated_data = payment_schema.load(data)
        except ValidationError as err:
            return {
                "message": "Validation failed",
                "errors": err.messages
            }, 400

        try:
            result = PaymentService.create(validated_data)
        except ValueError as err:
            return {
                "message": str(err)
            }, 400

        return payment_schema.dump(result), 201


class PaymentResource(Resource):

    def get(self, payment_id):
        try:
            payment = PaymentService.get_by_id(payment_id)
        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return payment_schema.dump(payment), 200

    def put(self, payment_id):
        data = request.get_json()

        if not data:
            return {
                "message": "Request body must contain JSON data"
            }, 400

        try:
            validated_data = payment_schema.load(
                data,
                partial=True
            )
        except ValidationError as err:
            return {
                "message": "Validation failed",
                "errors": err.messages
            }, 400

        try:
            result = PaymentService.update(
                payment_id,
                validated_data
            )
        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return {
            "message": "Payment updated successfully",
            "payment": payment_schema.dump(result)
        }, 200

    def delete(self, payment_id):
        try:
            PaymentService.delete(payment_id)
        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return {
            "message": "Payment deleted successfully"
        }, 200


class PaymentsByInvoiceResource(Resource):

    def get(self, invoice_id):
        try:
            payments = PaymentService.get_by_invoice_id(invoice_id)
        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return payment_schema.dump(
            payments,
            many=True
        ), 200