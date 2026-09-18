from marshmallow import Schema, fields


class AppointmentSchema(Schema):

    id = fields.Integer(dump_only=True)

    patient_id = fields.Integer(required=True)

    doctor_id = fields.Integer(required=True)

    appointment_date = fields.Date(required=True)

    appointment_time = fields.Time(required=True)

    reason = fields.String(required=False,allow_none=True)

    status = fields.String(required=False)

    created_at = fields.DateTime(dump_only=True)

    updated_at = fields.DateTime(dump_only=True)


appointment_schema = AppointmentSchema()