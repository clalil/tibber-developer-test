from app.api import app
import json
import pytest

@pytest.fixture()
def robot_app():
    app.config.update({
        "TESTING": True,
    })
    yield app

def test__when_moving__should_not_go_outside_world_boundary():
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
