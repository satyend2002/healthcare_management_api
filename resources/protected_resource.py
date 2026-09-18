from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, get_jwt
from utils.role_required import role_required


class ProtectedResource(Resource):

    @role_required("admin")
    def get(self):

        user_id = get_jwt_identity()
        claims = get_jwt()

        return {
            "message": "Admin access granted",
            "user_id": user_id,
            "username": claims.get("username"),
            "role": claims.get("role")
        }, 200