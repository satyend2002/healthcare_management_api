from models.inventory_transaction import InventoryTransaction
from models.medicine import Medicine
from repositories.inventory_transaction_repository import (
    InventoryTransactionRepository
)


class InventoryTransactionService:
    
    @staticmethod
    def create(data):
        medicine = Medicine.query.get(data["medicine_id"])

        if not medicine:
            raise ValueError("Medicine not found")

        transaction_type = data["transaction_type"]
        quantity = data["quantity"]

        if transaction_type not in ["stock_in", "stock_out"]:
            raise ValueError(
                "Transaction type must be stock_in or stock_out"
            )

        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero"
            )

        if transaction_type == "stock_out":
            if quantity > medicine.stock_quantity:
                raise ValueError(
                    "Insufficient medicine stock"
                )

            medicine.stock_quantity -= quantity

        elif transaction_type == "stock_in":
            medicine.stock_quantity += quantity

        transaction = InventoryTransaction(
            medicine_id=data["medicine_id"],
            transaction_type=transaction_type,
            quantity=quantity,
            reference=data.get("reference"),
            notes=data.get("notes"),
            transaction_date=data.get("transaction_date")
        )

        return InventoryTransactionRepository.create(transaction)

    @staticmethod
    def get_by_id(transaction_id):
        transaction = InventoryTransactionRepository.get_by_id(
            transaction_id
        )

        if not transaction:
            raise ValueError(
                "Inventory transaction not found"
            )

        return transaction

    @staticmethod
    def get_all():
        return InventoryTransactionRepository.get_all()

    @staticmethod
    def get_by_medicine_id(medicine_id):
        medicine = Medicine.query.get(medicine_id)

        if not medicine:
            raise ValueError("Medicine not found")

        return InventoryTransactionRepository.get_by_medicine_id(
            medicine_id
        )

    @staticmethod
    def update(transaction_id, data):
        transaction = InventoryTransactionService.get_by_id(
            transaction_id
        )

        if "medicine_id" in data:
            medicine = Medicine.query.get(data["medicine_id"])

            if not medicine:
                raise ValueError("Medicine not found")

            transaction.medicine_id = data["medicine_id"]

        if "transaction_type" in data:
            if data["transaction_type"] not in [
                "stock_in",
                "stock_out"
            ]:
                raise ValueError(
                    "Transaction type must be stock_in or stock_out"
                )

            transaction.transaction_type = data["transaction_type"]

        if "quantity" in data:
            if data["quantity"] <= 0:
                raise ValueError(
                    "Quantity must be greater than zero"
                )

            transaction.quantity = data["quantity"]

        if "reference" in data:
            transaction.reference = data["reference"]

        if "notes" in data:
            transaction.notes = data["notes"]

        if "transaction_date" in data:
            transaction.transaction_date = data["transaction_date"]

        return InventoryTransactionRepository.update(transaction)

    @staticmethod
    def delete(transaction_id):
        transaction = InventoryTransactionService.get_by_id(
            transaction_id
        )

        InventoryTransactionRepository.delete(transaction)

        return True