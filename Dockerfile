FROM python:3.12-bullseye
WORKDIR /src
COPY . .
EXPOSE 5000
RUN pip3 install -r requirements.txt

CMD ["flask", "--app", "src/api", "run", "--host=0.0.0.0"]
