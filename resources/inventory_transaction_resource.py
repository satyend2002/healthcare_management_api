from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from schemas.inventory_transaction_schema import (
    inventory_transaction_schema
)
from services.inventory_transaction_service import (
    InventoryTransactionService
)


class InventoryTransactionListResource(Resource):

    def get(self):
        transactions = InventoryTransactionService.get_all()

        return inventory_transaction_schema.dump(
            transactions,
            many=True
        ), 200

    def post(self):
        data = request.get_json()

        if not data:
            return {
                "message": "Request body must contain JSON data"
            }, 400

        try:
            validated_data = inventory_transaction_schema.load(data)

        except ValidationError as err:
            return {
                "message": "Validation failed",
                "errors": err.messages
            }, 400

        try:
            result = InventoryTransactionService.create(
                validated_data
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 400

        return inventory_transaction_schema.dump(result), 201


class InventoryTransactionResource(Resource):

    def get(self, transaction_id):
        try:
            transaction = InventoryTransactionService.get_by_id(
                transaction_id
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return inventory_transaction_schema.dump(
            transaction
        ), 200

    def put(self, transaction_id):
        data = request.get_json()

        if not data:
            return {
                "message": "Request body must contain JSON data"
            }, 400

        try:
            validated_data = inventory_transaction_schema.load(
                data,
                partial=True
            )

        except ValidationError as err:
            return {
                "message": "Validation failed",
                "errors": err.messages
            }, 400

        try:
            result = InventoryTransactionService.update(
                transaction_id,
                validated_data
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return {
            "message": "Inventory transaction updated successfully",
            "transaction": inventory_transaction_schema.dump(result)
        }, 200

    def delete(self, transaction_id):
        try:
            InventoryTransactionService.delete(transaction_id)

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return {
            "message": "Inventory transaction deleted successfully"
        }, 200


class InventoryTransactionsByMedicineResource(Resource):

    def get(self, medicine_id):
        try:
            transactions = (
                InventoryTransactionService.get_by_medicine_id(
                    medicine_id
                )
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return inventory_transaction_schema.dump(
            transactions,
            many=True
        ), 200