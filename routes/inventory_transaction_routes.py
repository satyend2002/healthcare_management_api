from flask import Blueprint
from flask_restful import Api

from resources.inventory_transaction_resource import (
    InventoryTransactionListResource,
    InventoryTransactionResource,
    InventoryTransactionsByMedicineResource
)


inventory_transaction_bp = Blueprint(
    "inventory_transaction",
    __name__,
    url_prefix="/api/v1/inventory-transactions"
)

inventory_transaction_api = Api(inventory_transaction_bp)

inventory_transaction_api.add_resource(
    InventoryTransactionListResource,
    ""
)

inventory_transaction_api.add_resource(
    InventoryTransactionResource,
    "/<int:transaction_id>"
)

inventory_transaction_api.add_resource(
    InventoryTransactionsByMedicineResource,
    "/medicine/<int:medicine_id>"
)