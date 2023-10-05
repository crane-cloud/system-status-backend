from marshmallow import Schema, fields


class StatusSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True)
    parent_name = fields.String(required=True)
    status = fields.String(required=True)
    description = fields.String()
    date_created = fields.Date(dump_only=True)
