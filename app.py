# from flask import  Flask, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_restful import Api
# from resources.health import Health
# from config import Config
# # from flask_migrate import Migrate 
# # from models.patient import Patient
# from extensions.extensions import db, migrate
# from resources.patient import PatientResource,PatientDetailResource
# from resources.department import DepartmentResource,DepartmentDetailResource
# from resources.doctor import DoctorResource, DoctorDetailResource

# app = Flask(__name__)
# app.config.from_object(Config) # Loading cofigurations ....
# api = Api(app)

# # db = SQLAlchemy(app) # Initializing database connection with the app ...  # due to circular import issues moving db and migrate to extensions/extensions.py file 
# # migrate = Migrate(app, db) # Initializing database migration with the app ......
# db.init_app(app)
# migrate.init_app(app, db)


# ## Registering resource with the endpoint using Flask RestApi ...
# api.add_resource(Health, "/health")
# api.add_resource(PatientResource,"/api/v1/patients")
# api.add_resource(PatientDetailResource,"/api/v1/patients/<int:patient_id>")

# api.add_resource(DepartmentResource, "/api/v1/departments")
# api.add_resource(DoctorResource,"/api/v1/doctors")

# api.add_resource(DoctorDetailResource,"/api/v1/doctors/<int:doctor_id>")
# api.add_resource(DepartmentDetailResource,"/api/v1/departments/<int:department_id>")


# @app.route("/")
# def home():
#     return jsonify(
#         message="Healthcare Management API is running"
#     )

# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, jsonify
from flask_restful import Api

from resources.health import Health
from config import Config
from extensions.extensions import db, migrate

from resources.department import (
    DepartmentResource,
    DepartmentDetailResource
)

from resources.doctor_resource import (
    DoctorResource,
    DoctorDetailResource
)
from flask_jwt_extended import JWTManager, get_jwt
from models.token_blocklist import TokenBlocklist
from flasgger import Swagger
from utils.error_handlers import register_error_handlers
from flask import Flask, jsonify
from flask_restful import Api
from werkzeug.exceptions import HTTPException

class CustomApi(Api):

    def handle_error(self, error):
        if isinstance(error, HTTPException):
            response = {
                "success": False,
                "message": error.description,
                "error": error.name,
                "status_code": error.code
            }

            return jsonify(response), error.code

        return super().handle_error(error)
app = Flask(__name__)

app.config.from_object(Config)  # Load configurations from Config class ....
jwt = JWTManager(app) # Initialize JWT Manager .....
register_error_handlers(app)

swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "Healthcare Management API",
        "description": "API documentation for the Healthcare Management System",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter: Bearer <your_access_token>"
        }
    }
})


@jwt.unauthorized_loader
def handle_missing_token(error):
    return {
        "message": "Authorization token is required"
    }, 401


@jwt.invalid_token_loader
def handle_invalid_token(error):
    return {
        "message": "Invalid authorization token"
    }, 401


@jwt.expired_token_loader
def handle_expired_token(jwt_header, jwt_payload):
    return {
        "message": "Authorization token has expired"
    }, 401


@jwt.revoked_token_loader
def handle_revoked_token(jwt_header, jwt_payload):
    return {
        "message": "Authorization token has been revoked"
    }, 401


@jwt.token_in_blocklist_loader # allowing users to logout and then again login and obtain refresh token and access token
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]

    token = TokenBlocklist.query.filter_by(jti=jti).first()

    return token is not None


@jwt.revoked_token_loader
def handle_revoked_token(jwt_header, jwt_payload):
    return {
        "message": "This token has been revoked. Please log in again."
    }, 401





from routes.patient_routes import patient_bp
from routes.Doctor_routes import doctor_bp
from routes.department_routes import department_bp
from routes.appointment_routes import appointment_bp
from routes.prescription_routes import prescription_bp
from routes.medicine_routes import medicine_bp 
from routes.prescription_item_routes import prescription_item_bp
from routes.medical_record_routes import medical_record_bp
from routes.invoice_routes import invoice_bp
from routes.patient_medical_history_routes import patient_medical_history_bp
from routes.payment_routes import payment_bp
from routes.inventory_transaction_routes import inventory_transaction_bp
from routes.lab_test_routes import lab_test_bp 
from routes.user_routes import user_bp
from routes.auth_routes import auth_bp
from routes.protected_routes import protected_bp



# Initialize Flask-RESTful ...
api = CustomApi(app, catch_all_404s=True)
    
# Initialize database and migration ........
db.init_app(app)
migrate.init_app(app, db)

# Health endpoint ......................
api.add_resource(
    Health,
    "/health"
)


# Register Patient Blueprint with flask/app............
app.register_blueprint(patient_bp) # connecting the patient blueprint to the main app .....

# Register Doctor Blueprint ...........
app.register_blueprint(doctor_bp)

# Register Department Blueprint ........
app.register_blueprint(department_bp)

# Register Appointment Blueprint .......
app.register_blueprint(appointment_bp)

# Register Prescription Blueprint ......
app.register_blueprint(prescription_bp)

# Register Medicine Blueprint ..........
app.register_blueprint(medicine_bp) 

# Register Prescription Item Blueprint ..........
app.register_blueprint(prescription_item_bp)

# Register Medical Record Blueprint ..........
app.register_blueprint(medical_record_bp) 

# Register Invoice Blueprint ..........
app.register_blueprint(invoice_bp) 


# Register Patient Medical History Blueprint ..........
app.register_blueprint(patient_medical_history_bp) 

# Register Payment Blueprint ..........
app.register_blueprint(payment_bp)

# Register Inventory_Transection Blueprint ..........
app.register_blueprint(inventory_transaction_bp)

# Register Lab Test Blueprint ..........
app.register_blueprint(lab_test_bp) 


# Register User Blueprint .......... 
app.register_blueprint(user_bp)  

# Register Auth Blueprint ..........
app.register_blueprint(auth_bp) 

# Register Protected Blueprint ..........
app.register_blueprint(protected_bp)

@app.route("/")
def home():
    return jsonify(
        message="Healthcare Management API is running"
    )


if __name__ == "__main__":
    app.run(debug=True)
    
