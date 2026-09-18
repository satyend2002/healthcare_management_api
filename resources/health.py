from flask_restful import Resource

class Health(Resource):

    def get(self):
        return {
            "status": "success",
            "message": "Healthcare API is healthy"
        } 
    
