from models.payment import Payment
from extensions.extensions import db


class PaymentRepository:

    @staticmethod
    def create(payment):
        db.session.add(payment)
        db.session.commit()
        return payment

    @staticmethod
    def get_by_id(payment_id):
        return Payment.query.get(payment_id)

    @staticmethod
    def get_all():
        return Payment.query.all()

    @staticmethod
    def get_by_invoice_id(invoice_id):
        return Payment.query.filter_by(invoice_id=invoice_id).all()

    @staticmethod
    def update(payment):
        db.session.commit()
        return payment

    @staticmethod
    def delete(payment):
        db.session.delete(payment)
        db.session.commit()