from marshmallow import Schema, fields

class NoteSchema(Schema):
    id = fields.Int(dump_only=True)
    content = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    contact_id = fields.Int(required=True)