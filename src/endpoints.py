from flask import current_app as app
from flask_apispec.views import MethodResource
from flask_apispec import doc, use_kwargs
from flask_restful import Resource
from webargs.flaskparser import abort
from src.service import CleanPredictionService
from src.schemas import CleanPredictionRequest
from src.lib.jsonapi.errors import ClientAPIError

class CleanPredictionsAPI(Resource, MethodResource):

    @doc(description='Get Min/Max/Sum of Housekeeping Clean Prediction Times given a list of Clean UUIDs', tags=['Clean'])
    @use_kwargs(CleanPredictionRequest)
    def post(self, clean_ids):
        """ 
            :clean_ids  [String<UUID>]
        """
        try:
            return CleanPredictionService().get_min_max_sum(list(set(clean_ids)))
        except ClientAPIError as e:
            app.logger.error(e)
            abort(e.status, errors=e.message)
