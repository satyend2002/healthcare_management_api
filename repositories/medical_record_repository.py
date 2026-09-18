from models.medical_record import MedicalRecord
from extensions.extensions import db


class MedicalRecordRepository:

    @staticmethod
    def create(medical_record):
        db.session.add(medical_record)
        db.session.commit()
        return medical_record

    @staticmethod
    def get_by_id(medical_record_id):
        return MedicalRecord.query.get(medical_record_id)

    @staticmethod
    def get_all():
        return MedicalRecord.query.all()

    @staticmethod
    def get_by_patient_id(patient_id):
        return MedicalRecord.query.filter_by(
            patient_id=patient_id
        ).all()

    @staticmethod
    def update(medical_record):
        db.session.commit()
        return medical_record

    @staticmethod
    def delete(medical_record):
        db.session.delete(medical_record)
        db.session.commit()