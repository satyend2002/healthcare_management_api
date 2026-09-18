from marshmallow import Schema, fields


class DoctorSchema(Schema):

    id = fields.Integer(dump_only=True)

    first_name = fields.String(required=True)

    last_name = fields.String(required=True)

    specialization = fields.String(required=True)

    phone = fields.String(required=True)

    email = fields.Email(required=True)

    department_id = fields.Integer(required=True)

    created_at = fields.DateTime(dump_only=True)

    updated_at = fields.DateTime(dump_only=True)


doctor_schema = DoctorSchema()