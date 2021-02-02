from flask import Flask, Blueprint, jsonify
from flask_restful import Api
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
<<<<<<< HEAD
from src.extension import PatchedFlaskApiSpec as FlaskApiSpec

=======
from flask_apispec.extension import FlaskApiSpec
>>>>>>> main
from webargs.flaskparser import parser, abort
from src.endpoints import CleanPredictionsAPI

app = Flask(__name__)
blueprint = Blueprint('api', __name__)
api = Api(blueprint)
app.register_blueprint(blueprint)
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
<<<<<<< HEAD

=======
>>>>>>> main
docs = FlaskApiSpec(app)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '404 Not Found'}), 404

@parser.error_handler
def handle_request_validation_error(err, req, schema, error_status_code, error_headers):
    abort(400, errors=err.messages)

api.add_resource(CleanPredictionsAPI, '/cleans/predictions')
docs.register(CleanPredictionsAPI, blueprint='api')