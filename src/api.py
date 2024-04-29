from flask import Flask, request
import datetime as datetime
import json
import os
import sqlite3
import time
import pdb

ENV = os.getenv("ENIRONMENT", "LOCAL")
USE_DB = ""

if ENV == "LOCAL":
    USE_DB == "production_local.db"
elif ENV == "PROD":
    USE_DB == "production.db"

app = Flask(__name__)

SQL_CREATE_DB_TABLE = '''CREATE TABLE IF NOT EXISTS robot (
        id INTEGER PRIMARY KEY,
        timestamp DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime')), 
        commands INT, 
        result INT, 
        duration REAL)'''

SQL_INSERT_VALUES = 'INSERT INTO robot (timestamp, commands, result, duration) VALUES(?,?,?,?)'


class DataBase:
    def __init__(self, timestamp, commands, result, duration):
        self.timestamp = timestamp
        self.commands = commands
        self.result = result
        self.response = {"status_code": 200, "message": None}
        self.duration = duration
        self.db_rows = []


    def setup_db(self):
        pdb.set_trace()
        connection = sqlite3.connect(USE_DB)
        with connection:
            try:
                connection.execute(SQL_CREATE_DB_TABLE)
            except sqlite3.Error as e:
                print(f"Error: Database could not be initialized. Due to {e}")

    def save_to_db(self):
        connection = sqlite3.connect("production_db")
        with connection:
            try:
                connection.execute(SQL_INSERT_VALUES, (self.timestamp, self.commands, self.result, self.duration))
                print("Successfully entered values into Database")
                self.response["status_code"] = 201
            except sqlite3.Error as e:
                print(f"Error: Failed to enter values into Database due to: {e}")
                self.response["status_code"] = 500
                self.response["message"] = "Internal Service Error [500]: Failed to enter values into Database."

    def read_from_db(self):
        connection = sqlite3.connect("production_db")
        with connection:
            try:
                rows = connection.execute('SELECT * FROM robot').fetchall()
                self.db_rows.extend(rows)
                self.response["status_code"] = 201
            except sqlite3.Error as e:
                print(f"Error: Failed to read values into Database due to: {e}")
                self.response["status_code"] = 500
                self.response["message"] = "Internal Service Error [500]: Failed to read values from Database."
            return self.db_rows, self.response


class EndpointClient:
    def __init__(self, x, y, moves):
        self.x = x
        self.y = y
        self.moves = moves
        self.directions = {"north": 1, "east": 1, "south": -1, "west": -1}
        self.duration = None
        self.sum_moves = len(moves)
        self.unique_moves = 0

    @staticmethod
    def timestamp():
        return datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')

    def count_moves(self):
        start_time = time.perf_counter()
        coordinates = [(("x", self.x), ("y", self.y))]
        x = self.x
        y = self.y
        for move in self.moves:
            for step in range(move["steps"]):
                if move["direction"] == "east" or move["direction"] == "west":
                    x += self.directions[move["direction"]]
                    coordinates.append((("x", x), ("y", y)))
                if move["direction"] == "north" or move["direction"] == "south":
                    y += self.directions[move["direction"]]
                    coordinates.append((("x", x), ("y", y)))
        unique_moves = len(set(coordinates))
        self.duration = "{:.4f}".format(time.perf_counter() - start_time)
        return unique_moves, self.duration

    def run_robot(self):
        response = []
        unique_moves, duration = self.count_moves()
        return self.timestamp(), self.sum_moves, unique_moves, duration


def create_response_body(rows, status_code, message=None):
    response = [{"data":[], "status": status_code}]
    if message:
        response[0]["message"] = message
        return response
    else:
        for row in rows:
            response[0]["data"].append({
                "id": row[0],
                "timestamp": row[1],
                "commands": row[2],
                "result": row[3],
                "duration": row[4]
            })
    return response


def create_app_response_body(resp):
    x = resp["start"]["x"]
    y = resp["start"]["y"]
    moves = resp['commmands']
    client = EndpointClient(x, y, moves)
    timestamp, sum_commands, unique_moves, duration = client.run_robot()
    db = DataBase(timestamp, sum_commands, unique_moves, duration)

    db.setup_db()
    db.save_to_db()
    rows, db_response = db.read_from_db()

    result = create_response_body(rows, db_response["status_code"], db_response["message"])
    return result


@app.post("/tibber-developer-test/enter-path")
def create_request():
        if request.is_json:
            request_body = request.get_json(silent=False)
            response_body = create_app_response_body(request_body)

            response = app.response_class(
            response=json.dumps(response_body),
            status=200,
            mimetype='application/json'
        )

            return response
        return {"error": "Request must be JSON"}, 415


if __name__ == "__main__":
    if os.environ['FLASK_ENV'] == "production":
        app.run(host="0.0.0.0", port=5000, debug=False)
    if os.environ['FLASK_ENV'] == "development":
        app.run(host="0.0.0.0", port=5000, debug=True)


