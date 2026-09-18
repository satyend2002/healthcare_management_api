from marshmallow import Schema, fields


class MedicalRecordSchema(Schema):

    id = fields.Integer(dump_only=True)

    patient_id = fields.Integer(required=True)
    doctor_id = fields.Integer(required=True)
    appointment_id = fields.Integer(required=False, allow_none=True)

    diagnosis = fields.String(required=True)
    symptoms = fields.String(required=False, allow_none=True)
    treatment = fields.String(required=False, allow_none=True)
    notes = fields.String(required=False, allow_none=True)

    record_date = fields.Date(required=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


medical_record_schema = MedicalRecordSchema()  
