from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)

    username = fields.String(required=True)

    email = fields.Email(required=True)

    password = fields.String(
        required=True,
        load_only=True
    )

    role = fields.String(required=False)

    is_active = fields.Boolean(dump_only=True)

    created_at = fields.DateTime(dump_only=True)

    updated_at = fields.DateTime(dump_only=True)


user_schema = UserSchema()