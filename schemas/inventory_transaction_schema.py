from marshmallow import Schema, fields


class InventoryTransactionSchema(Schema):
    id = fields.Integer(dump_only=True)

    medicine_id = fields.Integer(required=True)

    transaction_type = fields.String(required=True)

    quantity = fields.Integer(required=True)

    reference = fields.String(
        required=False,
        allow_none=True
    )

    notes = fields.String(
        required=False,
        allow_none=True
    )

    transaction_date = fields.DateTime(
        required=False
    )

    created_at = fields.DateTime(dump_only=True)

    updated_at = fields.DateTime(dump_only=True)


inventory_transaction_schema = InventoryTransactionSchema()