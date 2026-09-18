from marshmallow import Schema, fields


class PrescriptionItemSchema(Schema):
    id = fields.Integer(dump_only=True)

    prescription_id = fields.Integer(required=True)
    medicine_id = fields.Integer(required=True)

    dosage = fields.String(required=True)
    frequency = fields.String(required=True)
    duration = fields.String(required=True)
    instructions = fields.String(required=False, allow_none=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


prescription_item_schema = PrescriptionItemSchema()