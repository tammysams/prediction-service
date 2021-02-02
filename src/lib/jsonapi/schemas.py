from marshmallow import fields, Schema, ValidationError, INCLUDE

class ResourceSchema(Schema):
    attributes = fields.Dict(required=True)
    id = fields.UUID(required=True)
    relationships = fields.Dict(required=True)

    class Meta:
        unknown = INCLUDE

class JSONAPIResponseSchema(Schema):
    data = fields.List(fields.Nested(ResourceSchema), required=True)
    meta = fields.Dict(required=True)
    links = fields.Dict(required=True)