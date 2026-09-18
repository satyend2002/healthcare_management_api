from marshmallow import Schema, fields


class MedicineSchema(Schema):

    id = fields.Integer(dump_only=True)

    name = fields.String(required=True)

    generic_name = fields.String(
        required=False,
        allow_none=True
    )

    brand_name = fields.String(
        required=False,
        allow_none=True
    )

    strength = fields.String(
        required=False,
        allow_none=True
    )

    dosage_form = fields.String(
        required=False,
        allow_none=True
    )

    manufacturer = fields.String(
        required=False,
        allow_none=True
    )

    stock_quantity = fields.Integer(
        required=False
    )

    reorder_level = fields.Integer(
        required=False
    )

    active = fields.Boolean(
        required=False
    )

    created_at = fields.DateTime(
        dump_only=True
    )

    updated_at = fields.DateTime(
        dump_only=True
    )


medicine_schema = MedicineSchema()