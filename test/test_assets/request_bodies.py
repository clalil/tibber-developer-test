TWO_COMMANDS_REQUEST_BODY = {
    "start": {
        "x": 10,
        "y": 22 },
    "commmands": [{
        "direction": "east",
        "steps": 2},
        {"direction": "north",
        "steps": 1}]
    }


TRACK_BACK_REQUEST_BODY = {
    "start": {
        "x": 0,
        "y": 0 },
    "commmands": [{
        "direction": "east",
        "steps": 2},
        {"direction": "west",
        "steps": 2}]
    }

CROSS_TWICE_REQUEST_BODY = {
    "start": {
        "x": 0,
        "y": 0 },
    "commmands": [{
        "direction": "south",
        "steps": 2},
        {"direction": "east",
        "steps": 2},
        {"direction": "north",
        "steps": 1},
        {"direction": "west",
        "steps": 3},
        {"direction": "south",
        "steps": 1}]
    }