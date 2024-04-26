from flask import Flask, request

app = Flask(__name__)

@app.post('/tibber-developer-test/enter-path')
def create_room():
        response = request.get_json(silent=False)
        return response, 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
