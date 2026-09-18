from extensions.extensions import db
from models.patient import Patient
from sqlalchemy import or_

class PatientRepository:

    @staticmethod
    def get_all(page=1,per_page=10,search="",gender="",sort_by="id",order="asc"):
        query = Patient.query

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

        if gender:
            query = query.filter(Patient.gender.ilike(gender)) 

        allowed_sort_fields = {
            "id": Patient.id,
            "first_name": Patient.first_name,
            "last_name": Patient.last_name,
            "created_at": Patient.created_at
        }

        sort_column = allowed_sort_fields.get(sort_by, Patient.id)

        if order == "desc":
            query = query.order_by(sort_column.desc(), Patient.id.desc())
        else:
            query = query.order_by(sort_column.asc(), Patient.id.asc())

        return query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
            
            
    @staticmethod
    def get_by_id(patient_id):
        return db.session.get(Patient, patient_id)

    @staticmethod
    def get_by_phone(phone):
        return Patient.query.filter_by(phone=phone).first()

    @staticmethod
    def get_by_email(email):
        return Patient.query.filter_by(email=email).first()

    @staticmethod
    def create(patient):
        db.session.add(patient)
        db.session.commit()

        return patient

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(patient):
        db.session.delete(patient)
        db.session.commit()
        
