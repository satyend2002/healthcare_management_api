from marshmallow import Schema, fields


class DepartmentSchema(Schema):

    id = fields.Integer(dump_only=True)

    name = fields.String(required=True)

    description = fields.String(required=False,allow_none=True)

    created_at = fields.DateTime(dump_only=True)

    updated_at = fields.DateTime(dump_only=True)


department_schema = DepartmentSchema()