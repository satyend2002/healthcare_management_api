from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from schemas.medicine_schema import medicine_schema
from services.medicine_service import MedicineService
from flask_jwt_extended import jwt_required

class MedicineListResource(Resource):
    @jwt_required()
    def get(self):
        """
    Get a paginated list of medicines
    ---
    tags:
      - Medicines
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
      - name: search
        in: query
        type: string
        description: Search by medicine name, generic name, or brand
      - name: active
        in: query
        type: boolean
        description: Filter by active status
      - name: low_stock
        in: query
        type: boolean
        description: Show medicines below reorder level
      - name: sort_by
        in: query
        type: string
        default: id
      - name: order
        in: query
        type: string
        default: asc
        enum:
          - asc
          - desc
    responses:
      200:
        description: Medicines retrieved successfully
      400:
        description: Invalid query parameters
      401:
        description: Missing or invalid access token
      403:
        description: Access denied
    """
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)
        if page < 1:
            return {
                "message": "Page must be greater than or equal to 1"
            }, 400

        if per_page < 1:
            return {
                "message": "Per page must be greater than 0"
            }, 400
            
        search = request.args.get(
            "search",
            default="",
            type=str
        ).strip()

        active = request.args.get(
            "active",
            default=None,
            type=str
        )

        low_stock = request.args.get(
            "low_stock",
            default=None,
            type=str
        )

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

        result = MedicineService.get_all(
            page=page,
            per_page=per_page,
            search=search,
            active=active,
            low_stock=low_stock,
            sort_by=sort_by,
            order=order
        )

        return {
            "message": "Medicines retrieved successfully",
            "data": medicine_schema.dump(
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

    
    @jwt_required()
    def post(self):
        
        """
    Create a new medicine
    ---
    tags:
      - Medicines
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
            - name
            - stock
            - reorder_level
          properties:
            name:
              type: string
              example: Paracetamol
            generic_name:
              type: string
              example: Paracetamol
            brand:
              type: string
              example: Crocin
            strength:
              type: string
              example: 500 mg
            form:
              type: string
              example: Tablet
            stock:
              type: integer
              example: 100
            reorder_level:
              type: integer
              example: 10
            is_active:
              type: boolean
              example: true
    responses:
      201:
        description: Medicine created successfully
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
            validated_data = medicine_schema.load(data) 

        except ValidationError as err:
            return {
                "message": "Validation failed",
                "errors": err.messages
            }, 400

        try:
            result = MedicineService.create(
                validated_data
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 400

        return medicine_schema.dump(result), 201


class MedicineResource(Resource):
    @jwt_required()
    def get(self, medicine_id):
        """
    Get medicine details by ID
    ---
    tags:
      - Medicines
    security:
      - BearerAuth: []
    parameters:
      - name: medicine_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Medicine details retrieved successfully
      404:
        description: Medicine not found
      401:
        description: Missing or invalid access token
      403:
        description: Access denied
    """
        try:
            medicine = MedicineService.get_by_id(
                medicine_id
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return medicine_schema.dump(
            medicine
        ), 200
    
    @jwt_required()
    def put(self, medicine_id):
        """
    Update medicine details by ID
    ---
    tags:
      - Medicines
    security:
      - BearerAuth: []
    consumes:
      - application/json
    parameters:
      - name: medicine_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: Paracetamol
            stock:
              type: integer
              example: 150
            reorder_level:
              type: integer
              example: 10
            is_active:
              type: boolean
              example: true
    responses:
      200:
        description: Medicine updated successfully
      400:
        description: Validation failed
      404:
        description: Medicine not found
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
            validated_data = medicine_schema.load(
                data,
                partial=True
            )

        except ValidationError as err:
            return {
                "message": "Validation failed",
                "errors": err.messages
            }, 400

        try:
            result = MedicineService.update(
                medicine_id,
                validated_data
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 400

        return {
            "message": "Medicine updated successfully",
            "medicine": medicine_schema.dump(result)
        }, 200

    @jwt_required()
    def delete(self, medicine_id):
        """
    Delete medicine by ID
    ---
    tags:
      - Medicines
    security:
      - BearerAuth: []
    parameters:
      - name: medicine_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Medicine deleted successfully
      404:
        description: Medicine not found
      401:
        description: Missing or invalid access token
      403:
        description: Access denied
    """

        try:
            MedicineService.delete(
                medicine_id
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return {
            "message": "Medicine deleted successfully"
        }, 200 
