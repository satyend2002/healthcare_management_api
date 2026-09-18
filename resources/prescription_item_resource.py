from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from schemas.prescription_item_schema import prescription_item_schema
from services.prescription_item_service import PrescriptionItemService


class PrescriptionItemListResource(Resource):

    def get(self):
        """
    Get all prescription items
    ---
    tags:
      - Prescription Items
    security:
      - BearerAuth: []
    parameters:
      - name: prescription_id
        in: query
        type: integer
        required: false
        description: Filter items by prescription ID
      - name: medicine_id
        in: query
        type: integer
        required: false
        description: Filter items by medicine ID
    responses:
      200:
        description: Prescription items retrieved successfully
      401:
        description: Missing or invalid access token
      403:
        description: Access denied
    """

        prescription_items = PrescriptionItemService.get_all()

        return (
            prescription_item_schema.dump(
                prescription_items,
                many=True
            ),
            200
        )

    def post(self):
        """
    Add a medicine to a prescription
    ---
    tags:
      - Prescription Items
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
            - prescription_id
            - medicine_id
            - dosage
            - frequency
            - duration
          properties:
            prescription_id:
              type: integer
              example: 1
            medicine_id:
              type: integer
              example: 1
            dosage:
              type: string
              example: 500 mg
            frequency:
              type: string
              example: Twice daily
            duration:
              type: string
              example: 5 days
            instructions:
              type: string
              example: Take after meals
    responses:
      201:
        description: Prescription item created successfully
      400:
        description: Validation failed
      404:
        description: Prescription or medicine not found
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
            validated_data = prescription_item_schema.load(data)

        except ValidationError as err:
            return {
                "message": "Validation failed",
                "errors": err.messages
            }, 400

        try:
            result = PrescriptionItemService.create(
                validated_data
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return (
            prescription_item_schema.dump(result),
            201
        )


class PrescriptionItemResource(Resource):

    def get(self, prescription_item_id):
        """
    Get prescription item by ID
    ---
    tags:
      - Prescription Items
    security:
      - BearerAuth: []
    parameters:
      - name: item_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Prescription item retrieved successfully
      404:
        description: Prescription item not found
      401:
        description: Missing or invalid access token
      403:
        description: Access denied
    """
        try:
            prescription_item = (
                PrescriptionItemService.get_by_id(
                    prescription_item_id
                )
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return (
            prescription_item_schema.dump(
                prescription_item
            ),
            200
        )

    def put(self, prescription_item_id):
        """
    Update prescription item by ID
    ---
    tags:
      - Prescription Items
    security:
      - BearerAuth: []
    consumes:
      - application/json
    parameters:
      - name: item_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            dosage:
              type: string
              example: 500 mg
            frequency:
              type: string
              example: Once daily
            duration:
              type: string
              example: 7 days
            instructions:
              type: string
              example: Take after dinner
    responses:
      200:
        description: Prescription item updated successfully
      400:
        description: Validation failed
      404:
        description: Prescription item not found
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
            validated_data = prescription_item_schema.load(
                data,
                partial=True
            )

        except ValidationError as err:
            return {
                "message": "Validation failed",
                "errors": err.messages
            }, 400

        try:
            result = PrescriptionItemService.update(
                prescription_item_id,
                validated_data
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return {
            "message": "Prescription item updated successfully",
            "prescription_item": prescription_item_schema.dump(
                result
            )
        }, 200

    def delete(self, prescription_item_id):
        """
    Delete prescription item by ID
    ---
    tags:
      - Prescription Items
    security:
      - BearerAuth: []
    parameters:
      - name: item_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Prescription item deleted successfully
      404:
        description: Prescription item not found
      401:
        description: Missing or invalid access token
      403:
        description: Access denied
    """
        try:
            PrescriptionItemService.delete(
                prescription_item_id
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return {
            "message": "Prescription item deleted successfully"
        }, 200


class PrescriptionItemsByPrescriptionResource(Resource):

    def get(self, prescription_id):
        try:
            prescription_items = (
                PrescriptionItemService.get_by_prescription_id(
                    prescription_id
                )
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return (
            prescription_item_schema.dump(
                prescription_items,
                many=True
            ),
            200
        )