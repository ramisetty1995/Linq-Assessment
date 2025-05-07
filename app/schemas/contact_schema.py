from marshmallow import Schema, fields

class ContactSchema(Schema):
    id = fields.Int(dump_only=True)
    full_name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str()
    user_id = fields.Int(dump_only=True)