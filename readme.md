# Housekeeping Predictions

An extendable service that collects housekeeping clean prediction stats

## Stack
- Flask
- Serverless
- AWS Lambda
- API Gateway


# Features

### JSON-API Client Library
While there are many libraries for building a service that follows the json-api spec, I didn’t find any libraries for building clients of such a service that thrilled me -- so this service includes a draft jsonapi compatible client. 

This library leverages the consistency of the json-api spec and [marshmallow's](https://marshmallow.readthedocs.io/en/stable/) Schema/Field-type validation to safely encapsulate Request/Response logic. Example:
```python3
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
```

This eliminates most of boiler-plate code that would be needed each time a new client or endpoiint is added to this service.

```python3
class HouseKeepingClient(JSONAPIClient):
   base_url = "https://housekeeping.vacasa.io"
 
class CleansListAPI(ListAPI):
   client = HouseKeepingClient()
   resource = "cleans"
   query_schema = CleansQuerySchema()

```

### Batching of Requests
This service depends on the [housekeeping service](ekeeping.vacasa.io/#operation/cleans_list) (“cleans” resource). Following the JSON-API spec, the housekeeping service uses query params to filter resource UUIDs, which constrains the maximum number of UUIDs that can be filtered in a single request, before a max URL is reached (2,048 chars) or 175 uuids.

When a request contains on a long list of UUIDs, the list is de-duplicated and requests are sent in batches with a max of 175 UUIDs

*(even though the housekeeping ignores duplicates, we must dedup when batching, since duplicates could span multiple batches)

### Multi-Threading of Batched Requests
The JSON-API library created for this service leverages multi-threading to parallelize batched requests (outlined above) to improve total performance. This is additionally desirable to avoid time-outs, since AWS gateway imposes a hard-max of 30s before closing connections (which is adopted in our serverless.yml configuration). [note the different timescales below].

Batched requests totaling 3000 UUIDs
---
- **Before (8s)** 
![image](https://user-images.githubusercontent.com/37048195/106646344-7f204400-6542-11eb-882d-7ef31677f7b6.png)
- **After (3s)** 
![image](https://user-images.githubusercontent.com/37048195/106647009-3b7a0a00-6543-11eb-9a95-ba0bc068af7a.png)

**Tested at a max of 72,000 UUIDs before I hit a rate limit**
```bash
LENGTH REQUEST 72000
'get_min_max_sum'  11839.79 ms
127.0.0.1 - - [31/Jan/2021 22:54:28] "POST /cleans/predictions HTTP/1.1" 200 -

LENGTH REQUEST 72000
[2021-01-31 22:56:08,656] ERROR in endpoints:
127.0.0.1 - - [31/Jan/2021 22:56:08] "POST /cleans/predictions HTTP/1.1" 403 -
```


## Installation/Usage

Create a virtual env

```bash
virtualenv -p python3 venv
source venv/bin/activate
```
Clone the project

```bash
git@github.com:tammysams/prediction-service.git
```

Install requirements

```bash
pip install -r requirements.txt
```


Local Development

```bash
serverless wsgi serve
```

Run Tests

```bash
pytest
```

## API Documentation
[Swagger Docs](https://kjtxpgv5ei.execute-api.us-east-1.amazonaws.com/dev/docs/#/Clean) 

- Get Min/Max/Sum of Clean Prediction Times given a list of Clean UUIDs 
```
curl -POST "https://kjtxpgv5ei.execute-api.us-east-1.amazonaws.com/dev/cleans/predictions"
--data '{
"clean_ids":["e3e70682-c209-4cac-629f-6fbed82c07cd", "16a92bf5-0e5d-4372-a801-1d4e2895be65"]
}'
-H "Content-Type: application/json"
```