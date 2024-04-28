from flask import Flask, request, jsonify
import datetime as datetime
import sqlite3
import time
import pdb

app = Flask(__name__)

SQL_CREATE_DB_TABLE = '''CREATE TABLE IF NOT EXISTS robot (
        id INTEGER PRIMARY KEY,
        timestamp DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime')), 
        commands INT, 
        result INT, 
        duration REAL)'''


class DataBase:
    def __init__(self, timestamp, commands, result, duration):
        self.timestamp = timestamp
        self.commands = commands
        self.result = result
        self.response = {}
        self.duration = duration
        self.db_rows = []


    def setup_db(self):
        connection = sqlite3.connect("production_db")
        with connection:
            try:
                connection.execute(SQL_CREATE_DB_TABLE)
            except sqlite3.Error as e:
                print(f"Error: Database could not be initialized. Due to {e}")

    def save_to_db(self):
        connection = sqlite3.connect("production_db")
        with connection:
            try:
                connection.execute('INSERT INTO robot VALUES(?,?,?,?)', (self.timestamp, self.commands, self.result, self.duration))
                print("Successfully entered values into Database")
            except sqlite3.Error as e:
                print(f"Error: Failed to enter values into Database due to: {e}")
                self.response["status_code"] = 500
                self.response["error"] = "Internal Service Error [500]: Failed to enter values into Database."
                connection.rollback()

    def read_from_db(self):
        connection = sqlite3.connect("production_db")
        with connection:
            try:
                rows = connection.execute('SELECT * FROM robot').fetchall()
                self.db_rows.extend(rows)
            except sqlite3.Error as e:
                print(f"Error: Failed to enter values into Database due to: {e}")
                self.response["status_code"] = 500
                self.response["error"] = "Internal Service Error [500]: Failed to read values from Database."
            return self.db_rows


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


def create_response_body(rows):
    response = []
    for row in rows:
        response.append({
        "robot": {
            "id": row[0],
            "timestamp": row[1],
            "commands": row[2],
            "result": row[3],
            "duration": row[4]
        }
    })
    return response


def create_app_response_body(resp):
    x = resp["start"]["x"]
    y = resp["start"]["y"]
    moves = resp['commmands']
    client = EndpointClient(x, y, moves)
    timestamp, sum_commands, unique_moves, duration = client.run_robot()
    db = DataBase(timestamp, sum_commands, unique_moves, duration)

    # Save to DB & Read from DB
    db.save_to_db()
    rows = db.read_from_db()
    # pdb.set_trace()
    result = create_response_body(rows)
    return result


@app.post("/tibber-developer-test/enter-path")
def create_request():
        if request.is_json:
            request_body = request.get_json(silent=False)
            response_body = create_app_response_body(request_body)
            return jsonify(response_body), 201
        return {"error": "Request must be JSON"}, 415

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)


