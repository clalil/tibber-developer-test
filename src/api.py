from flask import Flask, request
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
        self.timestamp = ""
        self.unique_moves = 0

    # @staticmethod
    # def timestamp():
    #     return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')

    def get_coors(self, coordinates):
        x1 = coordinates[0][0][1]
        y1 = coordinates[0][1][1]
        x2 = coordinates[-1][0][1]
        y2 = coordinates[-1][1][1]

        return x1, y1, x2, y2
    
    def count_moves(self):
        coordinates = [(("x", self.x), ("y", self.y))]
        increment_x = self.x
        increment_y = self.y
        for move in self.moves:
            if move["direction"] == "east" or move["direction"] == "west":
                increment_x += self.directions[move["direction"]] * move["steps"]
                coordinates.extend([(("x", increment_x), ("y", increment_y))])
            if move["direction"] == "north" or move["direction"] == "south":
                increment_y += self.directions[move["direction"]] * move["steps"]
                coordinates.extend([(("x", increment_x), ("y", increment_y))])

        x1, y1, x2, y2 = self.get_coors(coordinates)
        path_travelled_between_cors = max(abs(x1 - x2),abs(y1 - y2))
            # calculate if move is unique


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
    response = client.count_moves()
    # print(f"Here is response: {client.count_moves()}")
    return resp

@app.post("/tibber-developer-test/enter-path")
def create_request():
        if request.is_json:
            request_body = request.get_json(silent=False)
            response_body = app_response_body(request_body)
            return response_body, 201
        return {"error": "Request must be JSON"}, 415

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)


