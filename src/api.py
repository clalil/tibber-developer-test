from flask import Flask, request, jsonify
import datetime as datetime
import time
# import pdb
# pdb.set_trace()
app = Flask(__name__)

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
                    x += 1
                    coordinates.append((("x", x), ("y", y)))
                if move["direction"] == "north" or move["direction"] == "south":
                    y += 1
                    coordinates.append((("x", x), ("y", y)))

        unique_moves = len(set(coordinates))

        return unique_moves


    def create_response_body(self):
        response_body = [{
            "result": {
                "timestamp": str(self.timestamp()),
                "commands": self.sum_moves,
                "result": self.count_moves(),
                "duration": 0.1
            }
        }]
        return response_body


# score = sum(base_rules[d].get(dice.count(d), 0) for d in set(dice))

    
    # for each move, update coordinates. 
    # make Set to distinguish unique
    # end time
    # create response

def app_response_body(resp):
    print(f"Here is request: {resp}")
    # print(f"Here is commands: {resp['commands']}")
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


