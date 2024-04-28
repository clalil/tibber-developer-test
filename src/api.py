from flask import Flask, request, jsonify
import datetime as datetime
import sqlite3
import time
import pdb

app = Flask(__name__)

SQL_CREATE_DB_TABLE = '''CREATE TABLE IF NOT EXISTS robot 
        (timestamp DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime')), 
        commands INT, 
        result INT, 
        duration REAL)'''


class DataBase:
    def __init__(self, timestamp, commands, result, duration):
        self.timestamp = timestamp
        self.commands = commands
        self.result = result
        self.duration = duration
        self.result = []

    # should store entry
    # should return entry
    @staticmethod
    def db():
        conn = sqlite3.connect("production_db")
        with conn:
            try:
                cursor = conn.cursor()
                cursor.execute(SQL_CREATE_DB_TABLE)
            except sqlite3.Error as e:
                print(f"Error: Database could not be initialized. Due to {e}")
                conn.rollback()
            yield conn

    def save_to_db(self):
        try:
            self.db.execute('INSERT INTO robot VALUES(?,?,?,?)', (self.timestamp, self.commands, self.result, self.duration))
            print("Suucessfully entered values into Database")
        except sqlite3.Error as e:
            print(f"Error: Failed to enter values into Database due to: {e}")
            self.db.rollback()

    def read_from_db(self):
        cursor = self.db.cursor()
        rows = cursor.fetchall()
        for row in rows:
            self.result.append(row)

class EndpointClient:
    def __init__(self, x, y, moves):
        self.x = x
        self.y = y
        self.moves = moves
        self.directions = {"north": 1, "east": 1, "south": -1, "west": -1}
        self.duration = 0
        self.sum_moves = len(moves)
        self.unique_moves = 0

    @staticmethod
    def timestamp():
        return datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')

    def count_moves(self):
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
        # pdb.set_trace()
        unique_moves = len(set(coordinates))
        return unique_moves

    def create_response_body(self):
        start_time = time.perf_counter()
        response_body = [{
            "robot": {
                "id": 0,
                "timestamp": str(self.timestamp()),
                "commands": self.sum_moves,
                "result": self.count_moves(),
                "duration": 0
            }
        }]
        duration_six_decimals = "{:.4f}".format(time.perf_counter() - start_time)
        response_body[0]["robot"]["duration"] = duration_six_decimals
        return response_body


def app_response_body(resp):
    x = resp["start"]["x"]
    y = resp["start"]["y"]
    moves = resp['commmands']
    client = EndpointClient(x, y, moves)
    resp_body = client.create_response_body()
    return resp_body


@app.post("/tibber-developer-test/enter-path")
def create_request():
        if request.is_json:
            request_body = request.get_json(silent=False)
            response_body = app_response_body(request_body)
            return jsonify(response_body), 201
        return {"error": "Request must be JSON"}, 415

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)


