from marshmallow import Schema, fields, validate


class ProductionResponse(Schema):
    oil = fields.Float(required=True)
    gas = fields.Float(required=True)
    brine = fields.Float(required=True)
