from marshmallow import fields, Schema, INCLUDE

class CleanPredictionRequest(Schema):
    clean_ids = fields.List(fields.UUID(), required=True)

CleansQuerySchema = Schema.from_dict(
    {"filter[id][in]": fields.Str(), "page[size]": fields.Int()}
)