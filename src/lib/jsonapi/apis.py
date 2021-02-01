import json
from itertools import chain
from functools import reduce
from marshmallow import Schema, ValidationError
from abc import ABC
from src.lib.jsonapi.client import JSONAPIClient

def implements(instance, cls):
    return issubclass(type(instance), cls) or type(instance)==cls

class ListAPI(ABC):

    def __init__(self):
        try:
            assert(all(map(lambda args: implements(*args), (
                    (self.client, JSONAPIClient), 
                    (self.query_schema, Schema), 
                    (self.resource, str),
                )))
            )
        except AssertionError as e:
            raise NotImplementedError()

    def _request(self, query_params):
        self._validate_query(query_params)
        return self.client.get(self.resource, query_params)

    def _validate_query(self, query_params):
        try:
            self.query_schema.load(query_params)
        except ValidationError as e:
            raise Exception(e)

    # Methods
    def all(self, query_params={}):
        queries = [query_params]
        data = []
        while queries:
            next_query = queries=queries.pop()
            response = self._request(next_query)
            data += response["data"]
            if response["meta"]["has_next"]:
                queries.append({
                    **next_query,
                    **{ "page[number]": response["meta"]["page"]+1}
                })
        return data

    def filter_by_id(self, ids=[]):
        queries = self.batch_queries(ids)
        result = map(self._request, queries)
        chained = chain(*[response['data'] for response in result])
        return list(chained)

    # Helpers
    @staticmethod
    def batch_queries(ids=[]):
        """
        Split list of ids into lists of at most 175 ids 
        """
        batches = [ids[i:i + 175] for i in range(0, len(ids), 175)]
        return list(map(ListAPI.build_id_query, batches))

    @staticmethod
    def build_id_query(ids=[]):
        id_string = reduce(lambda a,b: f"{a},{b}", ids) #stringify and join ids
        return {
            "filter[id][in]": id_string,
            "page[size]": 175
        }