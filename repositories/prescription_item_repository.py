from models.prescription_item import PrescriptionItem
from extensions.extensions import db


class PrescriptionItemRepository:

    @staticmethod
    def create(prescription_item):
        db.session.add(prescription_item)
        db.session.commit()
        return prescription_item

    @staticmethod
    def get_by_id(prescription_item_id):
        return PrescriptionItem.query.get(prescription_item_id)

    @staticmethod
    def get_all():
        return PrescriptionItem.query.all()

    @staticmethod
    def get_by_prescription_id(prescription_id):
        return PrescriptionItem.query.filter_by(
            prescription_id=prescription_id
        ).all()

    @staticmethod
    def update(prescription_item):
        db.session.commit()
        return prescription_item

    @staticmethod
    def delete(prescription_item):
        db.session.delete(prescription_item)
        db.session.commit()  