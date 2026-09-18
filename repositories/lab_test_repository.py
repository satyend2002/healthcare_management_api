from models.lab_test import LabTest
from extensions.extensions import db


class LabTestRepository:

    @staticmethod
    def create(lab_test):
        db.session.add(lab_test)
        db.session.commit()
        return lab_test

    @staticmethod
    def get_by_id(lab_test_id):
        return LabTest.query.get(lab_test_id)

    @staticmethod
    def get_all():
        return LabTest.query.all()

    @staticmethod
    def update(lab_test):
        db.session.commit()
        return lab_test

    @staticmethod
    def delete(lab_test):
        db.session.delete(lab_test)
        db.session.commit()