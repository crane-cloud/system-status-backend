from marshmallow import Schema, fields, validate


class ClusterSchema(Schema):

    id = fields.UUID(dump_only=True)
    name = fields.String(required=True)
    host = fields.String(required=True)
    token = fields.String(load_only=True, required=True)
    description = fields.String(required=True)
    prometheus_url = fields.Url()
    cost_modal_url = fields.Url()
    date_created = fields.Date(dump_only=True)
