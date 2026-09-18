from marshmallow import Schema, fields


class LabTestSchema(Schema):
    id = fields.Integer(dump_only=True)

    test_code = fields.String(required=True)

    test_name = fields.String(required=True)

    description = fields.String(
        required=False,
        allow_none=True
    )

    sample_type = fields.String(
        required=False,
        allow_none=True
    )

    price = fields.Decimal(
        as_string=True,
        required=False
    )

    active = fields.Boolean(
        required=False
    )

    created_at = fields.DateTime(dump_only=True)

    updated_at = fields.DateTime(dump_only=True)


lab_test_schema = LabTestSchema()