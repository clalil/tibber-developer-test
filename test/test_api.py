from src.api import app as flask_app 
from src.api import EndpointClient, create_response_body
from freezegun import freeze_time
from unittest.mock import patch
from src.api import DataBase
import json
import pytest
import pdb

from test_assets.request_bodies import (
    TWO_COMMANDS_REQUEST_BODY,
    TRACK_BACK_REQUEST_BODY,
    CROSS_TWICE_REQUEST_BODY
)
from test_assets.expected_responses import (
    TWO_COMMANDS_RESPONSE_BODY,
    TRACK_BACK_RESPONSE_BODY,
    CROSS_TWICE_RESPONSE_BODY
)

@pytest.fixture()
def app():
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app


def test__when_making_a_post__should_return_valid_(app):
    url = '/tibber-developer-test/enter-path'
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

    response_body = {
        "robot": {
            "id": 1,
            "timestamp": "2018-05-12 12:45:10.851596",
            "commands": 2,
            "result": 4,
            "duration": 0.000123
        }
    }

    with app.test_client() as c:
        response = c.post(url, json=request_body)
    assert json.loads(response.data) == response_body


def test__create_app_response_body():
    EXAMPLE_ROW = [(1, '2018-05-12 12:45:10.851596', 2, 4, 0.000123)]
    response = create_response_body(EXAMPLE_ROW, 201)
    assert response == TWO_COMMANDS_RESPONSE_BODY

@pytest.mark.parametrize(
    "request_body, response_body",
    [
        (TWO_COMMANDS_REQUEST_BODY, TWO_COMMANDS_RESPONSE_BODY),
        (TRACK_BACK_REQUEST_BODY, TRACK_BACK_RESPONSE_BODY),
        (CROSS_TWICE_REQUEST_BODY, CROSS_TWICE_RESPONSE_BODY)
    ]
)
@freeze_time("2018-05-12 12:45:10.851596")
def test__client_run_robot__should_return_summary_when_called(request_body, response_body):
    x = request_body["start"]["x"]
    y = request_body["start"]["y"]
    moves = request_body['commmands']
    client = EndpointClient(x, y, moves)
    timestamp, sum_commands, unique_moves, duration = client.run_robot()

    assert response_body[0]["data"][0]["timestamp"] == timestamp
    assert response_body[0]["data"][0]["commands"] == sum_commands
    assert response_body[0]["data"][0]["result"] == unique_moves


@pytest.mark.parametrize(
    "request_body, response_body",
    [
        (TWO_COMMANDS_REQUEST_BODY, TWO_COMMANDS_RESPONSE_BODY),
        (TRACK_BACK_REQUEST_BODY, TRACK_BACK_RESPONSE_BODY),
        (CROSS_TWICE_REQUEST_BODY, CROSS_TWICE_RESPONSE_BODY)
    ]
)
def test__client_run_robot__should_return_summary_when_called(request_body, response_body):
    x = request_body["start"]["x"]
    y = request_body["start"]["y"]
    moves = request_body['commmands']
    client = EndpointClient(x, y, moves)
    unique_moves, duration = client.count_moves()
    assert response_body[0]["data"][0]["result"] == unique_moves

