from models.prescription import Prescription
from extensions.extensions import db


class PrescriptionRepository:

    @staticmethod
    def create(prescription):
        db.session.add(prescription)
        db.session.commit()
        return prescription

    @staticmethod
    def get_by_id(prescription_id):
        return Prescription.query.get(prescription_id)

    @staticmethod
    def get_all(page=1, per_page=10):
        return Prescription.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

    @staticmethod
    def update(prescription):
        db.session.commit()
        return prescription

    @staticmethod
    def delete(prescription):
        db.session.delete(prescription)
        db.session.commit()