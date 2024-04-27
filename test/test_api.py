from src.api import app, EndpointClient
from freezegun import freeze_time
import json
import pytest
import pdb

@pytest.fixture()
def robot_app():
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture
def request_body():
    request_body = {
        "start": {
            "x": 10,
            "y": 22 },
        "commmands": [{
            "direction": "east",
            "steps": 2 },
            {"direction": "north",
            "steps": 1}]
        }
    return request_body


@pytest.fixture
def response_body():
    response_body = [{
    "robot": {
        "id": 1,
        "timestamp": "2018-05-12 12:45:10.851596",
        "commands": 2,
        "result": 4,
        "duration": 0.000123
        }
    }]
    return response_body

# def test__when_making_a_post__should_return_valid_():
#     url = '/tibber-developer-test/enter-path'
#     request_body = {
#             "start": {
#                 "x": 10,
#                 "y": 22 },
#             "commmands": [{
#                 "direction": "east",
#                 "steps": 2 },
#                 {"direction": "north",
#                 "steps": 1}]
#             }
    
#     response_body = {
#         "robot": {
#             "id": 1,
#             "timestamp": "2018-05-12 12:45:10.851596",
#             "commands": 2,
#             "result": 4,
#             "duration": 0.000123
#         }
#     }
    
#     with app.test_client() as c:
#         response = c.post(url, json=request_body)
#     assert json.loads(response.data) == response_body

@freeze_time("2018-05-12 12:45:10.851596")
def test__client_should_return_summary_when_called(request_body, response_body):
    x = request_body["start"]["x"]
    y = request_body["start"]["y"]
    moves = request_body['commmands']
    client = EndpointClient(x, y, moves)
    resp = client.create_response_body()
    # pdb.set_trace()
    assert response_body[0]["robot"]["id"] == resp[0]["robot"]["id"]
    assert response_body[0]["robot"]["timestamp"] == resp[0]["robot"]["timestamp"]
    assert response_body[0]["robot"]["commands"] == resp[0]["robot"]["commands"]
    assert response_body[0]["robot"]["result"] == resp[0]["robot"]["result"]
