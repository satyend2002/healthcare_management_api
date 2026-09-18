from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from utils.role_required import role_required

from schemas.appointment_schema import appointment_schema
from services.appointment_service import AppointmentService


class AppointmentListResource(Resource):

    # Get all appointments .........................
    @role_required("admin", "doctor", "receptionist")
    def get(self):
        """
    Get a paginated list of appointments
    ---
    tags:
      - Appointments
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
        description: Search by appointment reason or status
      - name: status
        in: query
        type: string
        description: Filter by appointment status
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
        description: Appointments retrieved successfully
      400:
        description: Invalid pagination parameters
      401:
        description: Missing or invalid access token
      403:
        description: Access denied
    """
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=10, type=int)

        search = request.args.get(
            "search",
            default="",
            type=str
        ).strip()

        status = request.args.get(
            "status",
            default="",
            type=str
        ).strip()

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

        result = AppointmentService.get_all(
            page=page,
            per_page=per_page,
            search=search,
            status=status,
            sort_by=sort_by,
            order=order
        )

        return {
            "message": "Appointments retrieved successfully",
            "data": appointment_schema.dump(
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

    # Create appointment ...............................
    def post(self):
        """
    Create a new appointment
    ---
    tags:
      - Appointments
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
            - appointment_date
          properties:
            patient_id:
              type: integer
              example: 1
            doctor_id:
              type: integer
              example: 1
            appointment_date:
              type: string
              format: date-time
              example: "2026-09-16T10:30:00"
            reason:
              type: string
              example: General consultation
            status:
              type: string
              example: Scheduled
    responses:
      201:
        description: Appointment created successfully
      400:
        description: Validation failed
      404:
        description: Related patient or doctor not found
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
            validated_data = appointment_schema.load(data)

        except ValidationError as err:
            return {
                "message": "Validation failed",
                "errors": err.messages
            }, 400

        try:
            result = AppointmentService.create(validated_data)

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return appointment_schema.dump(result), 201


class AppointmentResource(Resource):

    # Get appointment by ID .......................
    def get(self, appointment_id):
        """
    Get appointment details by ID
    ---
    tags:
      - Appointments
    security:
      - BearerAuth: []
    parameters:
      - name: appointment_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Appointment details retrieved successfully
      404:
        description: Appointment not found
      401:
        description: Missing or invalid access token
      403:
        description: Access denied
    """
       

        try:
            appointment = AppointmentService.get_by_id(
                appointment_id
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return appointment_schema.dump(appointment), 200


    # Update appointment  ..............................
    def put(self, appointment_id):
        """
    Update appointment details by ID
    ---
    tags:
      - Appointments
    security:
      - BearerAuth: []
    consumes:
      - application/json
    parameters:
      - name: appointment_id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            appointment_date:
              type: string
              format: date-time
              example: "2026-09-16T11:00:00"
            reason:
              type: string
              example: Follow-up consultation
            status:
              type: string
              example: Completed
    responses:
      200:
        description: Appointment updated successfully
      400:
        description: Validation failed
      404:
        description: Appointment not found
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
            validated_data = appointment_schema.load(
                data,
                partial=True
            )

        except ValidationError as err:
            return {
                "message": "Validation failed",
                "errors": err.messages
            }, 400

        try:
            result = AppointmentService.update(
                appointment_id,
                validated_data
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return {
            "message": "Appointment updated successfully",
            "appointment": appointment_schema.dump(result)
        }, 200


    # Delete appointment
    def delete(self, appointment_id):
        """
    Delete appointment by ID
    ---
    tags:
      - Appointments
    security:
      - BearerAuth: []
    parameters:
      - name: appointment_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Appointment deleted successfully
      404:
        description: Appointment not found
      401:
        description: Missing or invalid access token
      403:
        description: Access denied
    """

        try:
            AppointmentService.delete(appointment_id)

        except ValueError as err:
            return {
                "message": str(err)
            }, 404

        return {
            "message": "Appointment deleted successfully"
        }, 200