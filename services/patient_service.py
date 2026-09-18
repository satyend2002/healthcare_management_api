from sqlalchemy import or_

from extensions.extensions import db
from models.patient import Patient
from schemas.patient_schema import PatientSchema


class PatientService:

    @staticmethod
    def create_patient(data):
        try:
            patient = Patient(**data)

            db.session.add(patient)
            db.session.commit()
            db.session.refresh(patient)

            return PatientSchema().dump(patient)

        except Exception as e:
            db.session.rollback()
            print("CREATE PATIENT ERROR:", repr(e), flush=True)

            return {
                "success": False,
                "message": "Failed to create patient",
                "error": str(e)
            }, 500
            
        
    @staticmethod
    def get_patients(
        page=1,
        per_page=10,
        search=None,
        gender=None,
        sort_by="id",
        order="asc"
    ):
        query = Patient.query

        # Search by first name, last name, phone, or email
        if search:
            search_pattern = f"%{search}%"

            query = query.filter(
                or_(
                    Patient.first_name.ilike(search_pattern),
                    Patient.last_name.ilike(search_pattern),
                    Patient.phone.ilike(search_pattern),
                    Patient.email.ilike(search_pattern)
                )
            )

        # Filter by gender
        if gender:
            query = query.filter(Patient.gender == gender)

        # Allowed sorting fields
        allowed_sort_fields = {
            "id": Patient.id,
            "first_name": Patient.first_name,
            "last_name": Patient.last_name,
            "created_at": Patient.created_at
        }

        sort_column = allowed_sort_fields.get(
            sort_by,
            Patient.id
        )

        if order.lower() == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

        # Pagination
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        # Serialize Patient objects into dictionaries
        serialized_patients = PatientSchema(
            many=True
        ).dump(pagination.items)

        return {
            "items": serialized_patients,
            "total": pagination.total,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "pages": pagination.pages
        }

    @staticmethod
    def get_patient(patient_id):
        patient = db.session.get(Patient, patient_id)

        if not patient:
            return {
                "success": False,
                "message": "Patient not found"
            }, 404

        return PatientSchema().dump(patient), 200

    @staticmethod
    def update_patient(patient_id, data):
        patient = db.session.get(Patient, patient_id)

        if not patient:
            return {
                "success": False,
                "message": "Patient not found"
            }, 404

        try:
            for key, value in data.items():
                if hasattr(patient, key):
                    setattr(patient, key, value)

            db.session.commit()
            db.session.refresh(patient)

            return PatientSchema().dump(patient), 200

        except Exception as e:
            db.session.rollback()

            return {
                "success": False,
                "message": "Failed to update patient",
                "error": str(e)
            }, 500

    @staticmethod
    def delete_patient(patient_id):
        patient = db.session.get(Patient, patient_id)

        if not patient:
            return {
                "success": False,
                "message": "Patient not found"
            }, 404

        try:
            db.session.delete(patient)
            db.session.commit()

            return None

        except Exception as e:
            db.session.rollback()

            return {
                "success": False,
                "message": "Failed to delete patient",
                "error": str(e)
            }, 500