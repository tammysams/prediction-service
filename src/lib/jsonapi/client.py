from marshmallow import ValidationError
import requests
from src.lib.jsonapi.errors import ClientAPIError
from src.lib.jsonapi.schemas import JSONAPIResponseSchema

class JSONAPIClient:
    HEADERS = {
        'Content-Type': 'application/vnd.api+json'
    }

    def get(self, endpoint, query_params={}, extra_headers={}):
        url = f"{self.base_url}/{endpoint}"
        headers = { **self.HEADERS, **extra_headers }
        response = requests.get(url, params=query_params, headers=headers)
        if not response.ok:
            raise ClientAPIError(f"Could not get {endpoint}.", f"{response.status_code}:{response.reason}", response.status_code)
        try:
            JSONAPIResponseSchema().load(response.json())
        except ValidationError as err:
            raise ClientAPIError(f"Error parsing {endpoint} data.", err, response.status_code)

        return response.json()

    def post(self, endpoint, payload, extra_headers={}):
        pass

    def patch(self, endpoint, payload, extra_headers={}):
        pass

    def delete(self, endpoint, query_params={}, extra_headers={}):
        pass