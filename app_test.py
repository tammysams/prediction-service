import pytest
from unittest.mock import patch
from app import app
from src.service import CleanPredictionService as service


@pytest.fixture
def client():
    return app.test_client()

def test_not_found_route(client):
    response = client.get('/not-found-route')
    json = response.get_json()
    assert json['error'] == '404 Not Found'

def test_clean_prediction_method_not_allowed(client):
    response = client.get('/cleans/predictions')
    json = response.get_json()
    assert json['message'] == 'The method is not allowed for the requested URL.'

def test_clean_prediction_missing_data(client):
    response = client.post('/cleans/predictions')
    json = response.get_json()
    assert json['errors'] == {'json': {'clean_ids': ['Missing data for required field.']}}

def test_clean_prediction_bad_data(client):
    data = {"clean_ids": ["123"]}
    response = client.post('/cleans/predictions', json = data)
    json = response.get_json()
    assert json['errors'] == {'json': {'clean_ids': {'0': ['Not a valid UUID.']}}}

mock = {'max': 2.91691406956171, 'min': 2.51412196030228, 'sum': 5.43103602986399}
@patch.object(service, 'get_min_max_sum', lambda *args: mock)
def test_clean_prediction_correct_data(client):
    data = {"clean_ids": ["e3e70682-c209-4cac-629f-6fbed82c07cd", "16a92bf5-0e5d-4372-a801-1d4e2895be65"]}
    response = client.post('/cleans/predictions', json = data)
    assert response.status_code == 200
    assert response.get_json() == mock
