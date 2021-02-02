# TODO: Stubbing out test plan here

# FIXTURES:

#   - CLEAN_IDS = [~3000 UUIDs]
#   - BATCHED_QUERIES = [
#       "?filter[id][in]=[...175 UUID batch]",
#       "?filter[id][in]=[...175 UUID batch]",
#       "?filter[id][in]=[...175 UUID batch]"
#     ]

#   - BATCHED_RESPONSES = [[ 175 response objects], [175 response objects]...]

# JSONAPI_Test_Harness:

# 	def get_mock_resource(id=randomUUID, attributes={}, relationships={}):
# 		return {
# 			"id": id,
# 			"attributes": attributes,
# 			"relationships": {}
# 		}

# 	def get_mock_response(resource_params=[{}], meta={}, links={}):
# 		return {
# 			"data": [get_mock_resource(param_obj) for param_obj in resource_params],
# 			"meta": meta,
# 			"links": links
# 		}

#   ## "register" endpoints for each of BATCHED_QUERIES to respond
#       with one of the BATCHED_RESPONSES



# LISTAPI_Test:

#   Use pytest autospec to assert that when LISTAPI.filter_by_id is given CLEAN_IDS:
#       - JSONAPI.get is called number of times exactly equal to len(BATCHED_QUERIES)
#       - JSONAPI.get is called with each of the BATCHED_QUERIES
#       - JSONAPI.get returns a single list of resource objects equal to sum
#         of lengths of BATCHED_RESPONSES

#   Unit test query batching and formating methods