from marshmallow import Schema, fields


class PrescriptionSchema(Schema):
    id = fields.Integer(dump_only=True)

    patient_id = fields.Integer(required=True)

    doctor_id = fields.Integer(required=True)

    appointment_id = fields.Integer(required=True)

    medicine_name = fields.String(required=True)

    dosage = fields.String(required=True)

    frequency = fields.String(required=True)

    duration = fields.String(required=True)

    instructions = fields.String(
        required=False,
        allow_none=True
    )

    created_at = fields.DateTime(dump_only=True)

    updated_at = fields.DateTime(dump_only=True)


prescription_schema = PrescriptionSchema()