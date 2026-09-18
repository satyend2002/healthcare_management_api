from marshmallow import Schema, fields


class InvoiceSchema(Schema):

    id = fields.Integer(dump_only=True)

    invoice_number = fields.String(
        required=True
    )

    patient_id = fields.Integer(
        required=True
    )

    appointment_id = fields.Integer(
        required=False,
        allow_none=True
    )

    subtotal = fields.Decimal(
        as_string=True,
        required=False
    )

    tax = fields.Decimal(
        as_string=True,
        required=False
    )

    discount = fields.Decimal(
        as_string=True,
        required=False
    )

    total_amount = fields.Decimal(
        as_string=True,
        required=False
    )

    payment_status = fields.String(
        required=False
    )

    due_date = fields.Date(
        required=False,
        allow_none=True
    )

    created_at = fields.DateTime(
        dump_only=True
    )

    updated_at = fields.DateTime(
        dump_only=True
    )


invoice_schema = InvoiceSchema()