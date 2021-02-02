from src.schemas import CleansQuerySchema
from src.lib.jsonapi.client import JSONAPIClient
from src.lib.jsonapi.apis import ListAPI

class HouseKeepingClient(JSONAPIClient):
    base_url = "https://housekeeping.vacasa.io"

class CleansListAPI(ListAPI):
    client = HouseKeepingClient()
    resource = "cleans"
    query_schema = CleansQuerySchema()

    def list_predictions(self, clean_ids=[]):
        clean_objs = self.filter_by_id(clean_ids)
        return [clean["attributes"]["predicted_clean_time"] for clean in clean_objs]
