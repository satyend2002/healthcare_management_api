from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from schemas.user_schema import user_schema
from services.user_service import UserService
from flask_jwt_extended import jwt_required
from utils.role_required import role_required


class UserRegistrationResource(Resource):

    def post(self):
        """
    Register a new user
    ---
    tags:
      - Users
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: newuser
            password:
              type: string
              example: StrongPassword123
            role:
              type: string
              example: user
    responses:
      201:
        description: User registered successfully
      400:
        description: Invalid request data
      409:
        description: Username already exists
    """

        data = request.get_json()

        if not data:
            return {
                "message": "Request body must contain JSON data"
            }, 400

        try:
            validated_data = user_schema.load(data)

        except ValidationError as err:
            return {
                "message": "Validation failed",
                "errors": err.messages
            }, 400

        try:
            user = UserService.register_user(
                validated_data
            )

        except ValueError as err:
            return {
                "message": str(err)
            }, 400

        return {
            "message": "User registered successfully",
            "user": user_schema.dump(user)
        }, 201


class UserListResource(Resource):
    
    @role_required("admin")
    def get(self):
        """
    Get all users
    ---
    tags:
      - Users
    security:
      - BearerAuth: []
    responses:
      200:
        description: List of users
      401:
        description: Authorization token is missing or invalid
      403:
        description: Access forbidden
    """
        users = UserService.get_all()

        return user_schema.dump(
            users,
            many=True
        ), 200


class AdminCreateUserResource(Resource):

    @role_required("admin")
    def post(self):
        """
    Create a user by administrator
    ---
    tags:
      - Users
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
            - username
            - password
          properties:
            username:
              type: string
              example: doctor3
            password:
              type: string
              example: StrongPassword123
            role:
              type: string
              example: doctor
    responses:
      201:
        description: User created successfully
      400:
        description: Invalid request data
      401:
        description: Authorization token is missing or invalid
      403:
        description: Admin access required
    """
        data = request.get_json()

        if not data:
            return {
                "message": "Request body must contain JSON data"
            }, 400

        try:
            user = UserService.create_user_by_admin(data)

            return {
                "message": "User created successfully by admin",
                "user": user_schema.dump(user)
            }, 201

        except ValueError as error:
            return {
                "message": str(error)
            }, 400        