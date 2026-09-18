from marshmallow import Schema, fields


class PaymentSchema(Schema):
    id = fields.Integer(dump_only=True)

    payment_reference = fields.String(required=True)

    invoice_id = fields.Integer(required=True)

    amount = fields.Decimal(
        as_string=True,
        required=True
    )

    payment_method = fields.String(required=True)

    payment_date = fields.DateTime(
        required=False
    )

    status = fields.String(
        required=False
    )

    notes = fields.String(
        required=False,
        allow_none=True
    )

    created_at = fields.DateTime(dump_only=True)

    updated_at = fields.DateTime(dump_only=True)


payment_schema = PaymentSchema()