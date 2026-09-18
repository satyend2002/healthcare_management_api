from models.inventory_transaction import InventoryTransaction
from extensions.extensions import db


class InventoryTransactionRepository:

    @staticmethod
    def create(transaction):
        db.session.add(transaction)
        db.session.commit()
        return transaction

    @staticmethod
    def get_by_id(transaction_id):
        return InventoryTransaction.query.get(transaction_id)

    @staticmethod
    def get_all():
        return InventoryTransaction.query.all()

    @staticmethod
    def get_by_medicine_id(medicine_id):
        return InventoryTransaction.query.filter_by(
            medicine_id=medicine_id
        ).all()

    @staticmethod
    def update(transaction):
        db.session.commit()
        return transaction

    @staticmethod
    def delete(transaction):
        db.session.delete(transaction)
        db.session.commit()