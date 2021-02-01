from flask import Flask
from flask_restful import Api
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from webargs.flaskparser import parser, abort
from src.endpoints import CleanPredictionsAPI

app = Flask(__name__)
api = Api(app)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Housekeeping Clean Prediction Aggregate',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/schema/',
    'APISPEC_SWAGGER_UI_URL': '/docs/'
})
docs = FlaskApiSpec(app)

@parser.error_handler
def handle_request_validation_error(err, req, schema, error_status_code, error_headers):
    abort(400, errors=err.messages)

api.add_resource(CleanPredictionsAPI, '/cleans/predictions')
docs.register(CleanPredictionsAPI)