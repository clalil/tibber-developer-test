# tibber-developer-test

## Author
[Clarissa Liljander](https://github.com/clalil)

## Built with
[Flask API](https://flask.palletsprojects.com/en/3.0.x/api/)
[sqlite3](https://sqlite.org/)

## About the project
This is a prototype microservice that simulates a robot moving around and cleaning the places it visits. The path of the robot's movement is described by the starting coordinates and move commands. After the cleaning has
been done, the robot reports the number of unique places cleaned. The service stores the results in the database and returns a JSON formatted response.

Due to heavy time contraints while doing this project sqlite3 was used to create a database. While SQLite offers a serverless, high-speed option, it lacks the robust capabilities needed for real-world applications like web development. Nevertheless, since this is a mere prototype (and it is possible to migrate your SQLite data into a PostgreSQL database) it was the optimal choice for me at the time.

Finally, I had a lot of fun building this project and learned a lot with tech (almost) completely new to me. And in the end, that's what it's all about. ^_^

## Getting started
### Setup
To test this application you need to fork it to your own GitHub account and clone it to your local workspace.
The code was written using python version 3.12.

#### Commands to get started locally on your own machine:
Create a virtual venv:
> python3 -m venv venv

Activate it:
> source venv/bin/activate

Install requirements:
> pip3 install -r requirements.txt

Choose which db to create:
> export ENVIRONMENT="LOCAL"

Run the tests:
> python -m pytest test

Start the app:
> flask --app src/api run

## Create a virtual machine using Docker
Build the image:
> docker build .

Start the container:
> docker run -p 5000:5000 -ti -d -e ENVIRONMENT=LOCAL <image_id>

Run commands inside the container:
> docker exec -ti <container_id> bash

Run the tests:
> python -m pytest test

Start making requests to the database, using the curl below:

#### Example curl:
```
curl --location 'http://127.0.0.1:5000/tibber-developer-test/enter-path' \
--header 'Content-Type: application/json' \
--data '{
    "start": {
        "x": 10,
        "y": 22 },
    "commmands": [{
        "direction": "east",
        "steps": 1},
        {"direction": "north",
        "steps": 12}]
}'
```

#### License
This project is released under the [MIT-license](https://en.wikipedia.org/wiki/MIT_License).