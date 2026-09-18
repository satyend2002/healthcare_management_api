from marshmallow import Schema, fields


class PatientSchema(Schema):

    id = fields.Integer(dump_only=True)

    first_name = fields.String(required=True)

    last_name = fields.String(required=True)

    date_of_birth = fields.Date(required=True)  

    gender = fields.String(required=True)

    phone = fields.String(required=True)

    email = fields.Email(required=True)

    address = fields.String(required=False, allow_none=True)

    created_at = fields.DateTime(dump_only=True)

    updated_at = fields.DateTime(dump_only=True)


patient_schema = PatientSchema()
    
    