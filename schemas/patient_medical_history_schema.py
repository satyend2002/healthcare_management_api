from marshmallow import Schema, fields


class PatientMedicalHistorySchema(Schema):

    id = fields.Integer(dump_only=True)

    patient_id = fields.Integer(
        required=True
    )

    history_type = fields.String(
        required=True
    )

    description = fields.String(
        required=True
    )

    diagnosis_date = fields.Date(
        required=False,
        allow_none=True
    )

    notes = fields.String(
        required=False,
        allow_none=True
    )

    created_at = fields.DateTime(
        dump_only=True
    )

    updated_at = fields.DateTime(
        dump_only=True
    )


patient_medical_history_schema = PatientMedicalHistorySchema()