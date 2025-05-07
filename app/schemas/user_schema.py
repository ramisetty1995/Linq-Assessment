from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3))
    password = fields.Str(load_only=True, required=True, validate=validate.Length(min=6))

class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)