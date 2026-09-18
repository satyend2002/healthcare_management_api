from flask import request
from flask_restful import Resource

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,get_jwt
)

from repositories.user_repository import UserRepository
from models.user import User
from models.token_blocklist import TokenBlocklist
from extensions.extensions import db

class LoginResource(Resource):
        
    def post(self):
        """
        User login
        ---
        tags:
          - Authentication
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
                  example: admin
                password:
                  type: string
                  example: Admin@123
        responses:
          200:
            description: Login successful
          401:
            description: Invalid credentials
        """
        data = request.get_json()

        if not data:
            return {
                "message": "Request body must contain JSON data"
            }, 400

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {
                "message": "Username and password are required"
            }, 400

        user = UserRepository.get_by_username(username) 

        if not user:
            return {
                "message": "Invalid username or password"
            }, 401

        if not user.is_active:
            return {
                "message": "User account is inactive"
            }, 403

        if not user.check_password(password):
            return {
                "message": "Invalid username or password"
            }, 401

        token_identity = str(user.id)

        additional_claims = {
            "username": user.username,
            "role": user.role
        }

        access_token = create_access_token(
            identity=token_identity,
            additional_claims=additional_claims
        )

        refresh_token = create_refresh_token(
            identity=token_identity,
            additional_claims=additional_claims
        )

        return {
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
        }, 200

class LogoutResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """
        Logout the current user
        ---
        tags:
          - Authentication
        security:
          - BearerAuth: []
        responses:
          200:
            description: Logout successful
          401:
            description: Missing or invalid access token
        """
        jwt_data = get_jwt()

        jti = jwt_data["jti"]
        token_type = jwt_data["type"]
        user_id = int(jwt_data["sub"])

        revoked_token = TokenBlocklist(
            jti=jti,
            token_type=token_type,
            user_id=user_id
        )

        db.session.add(revoked_token)
        db.session.commit()

        return {
            "message": "Logout successful. Refresh token has been revoked."
        }, 200
        
        

class RefreshTokenResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """
        Generate a new access token
        ---
        tags:
          - Authentication
        security:
          - BearerAuth: []
        responses:
          200:
            description: New access token generated successfully
          401:
            description: Invalid or expired refresh token
        """
        user_id = get_jwt_identity()

        user = UserRepository.get_by_id(int(user_id))

        if not user:
            return {
                "message": "User not found"
            }, 404

        if not user.is_active:
            return {
                "message": "User account is inactive"
            }, 403

        additional_claims = {
            "username": user.username,
            "role": user.role
        }

        new_access_token = create_access_token(
            identity=str(user.id),
            additional_claims=additional_claims
        )

        return {
            "message": "Access token refreshed successfully",
            "access_token": new_access_token
        }, 200        
        
        
class LogoutAccessTokenResource(Resource):
    @jwt_required()
    def post(self):
        """
        Logout using the current access token
        ---
        tags:
          - Authentication
        security:
          - BearerAuth: []
        responses:
          200:
            description: Access token revoked successfully
          401:
            description: Missing or invalid access token
        """
        jwt_data = get_jwt()

        jti = jwt_data["jti"]
        token_type = jwt_data["type"]
        user_id = int(jwt_data["sub"])

        revoked_token = TokenBlocklist(
            jti=jti,
            token_type=token_type,
            user_id=user_id
        )

        db.session.add(revoked_token)
        db.session.commit()

        return {
            "message": "Access token revoked successfully."
        }, 200
                
        