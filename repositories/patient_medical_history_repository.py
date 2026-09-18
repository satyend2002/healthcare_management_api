from models.patient_medical_history import PatientMedicalHistory
from extensions.extensions import db


class PatientMedicalHistoryRepository:

    @staticmethod
    def create(history):
        db.session.add(history)
        db.session.commit()
        return history

    @staticmethod
    def get_by_id(history_id):
        return PatientMedicalHistory.query.get(history_id)

    @staticmethod
    def get_all():
        return PatientMedicalHistory.query.all()

    @staticmethod
    def get_by_patient_id(patient_id):
        return PatientMedicalHistory.query.filter_by(
            patient_id=patient_id
        ).all()

    @staticmethod
    def update(history):
        db.session.commit()
        return history

    @staticmethod
    def delete(history):
        db.session.delete(history)
        db.session.commit()