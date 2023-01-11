# Brazilian 2022 Presidential Elections Predictor
elections-2022 is a project that collects and analyzes voting data from the official Brazilian elections website (https://resultados.tse.jus.br/oficial/app/index.html#/eleicao;e=e545/resultados). This project makes predictions for the Brazilian presidential elections in 2022. 

<img src="https://user-images.githubusercontent.com/56371504/199311177-78f666eb-2224-4ea0-867c-3586b4c6846e.png" alt="elections-2022" width="800"/>

# How It Works
The voting data is periodically collected from each Brazilian state. The data is then stored in a MongoDB database. The number of votes from each state is then extrapolated, considering that all the votes have been counted, and the vote proportion per candidate remained the same. The results of each state are then aggregated and a prediction is made. The predictions are stored in the database. The frontend consumes the predictions data via an API and displays the last prediction, as well as a graph showing all predictions over time.

# Installation
## For dockerized environment:
- Install Docker: https://docs.docker.com/get-docker/
- Install Docker Compose: https://docs.docker.com/compose/install/

## For local environment:
- Install MongoDB: https://www.mongodb.com/docs/manual/installation/
- Install Redis: https://redis.io/docs/getting-started/installation/
- Create a virtual environment:
```
$ python -m venv ./backend/.venv
``` 
- Activate the virtual environment:
```
$ . ./backend/.venv/bin/activate
```
- Install python dependencies:
```
$ pip install -r ./backend/requirements.txt
```

- Install npm dependencies:
```
$ npm --prefix ./frontend install ./frontend
```
# Usage

## For Dockerized environment:
- Start the containers:
```
$ make compose
```
- Start the containers with data collection:
```
$ make compose-collect
```
## For local environment:
- Start the API:
```
$ make api
```
- Start the UI:
```
$ make ui
```
- Start the worker:
```
$ make worker
```
- Start collecting data:
```
$ make collect
```
# Dependencies
- Python 3.8+
- MongoDB 4.0+
- Redis 6.0+
- npm 6.0+

# Known issues
- None at the moment.
