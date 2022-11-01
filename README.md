# Brazilian 2022 Presidential Elections Predictor
elections-2022 collects and analyzes data from the official brazilian elections website (https://resultados.tse.jus.br/oficial/app/index.html#/eleicao;e=e545/resultados).

# How It Works
Voting data is periodically collected from each brazilian state. <br/>
The number of votes from each state is then extrapolated, considering that all the votes have been counted, and the vote proportion per candidate remained the same. <br/>
The results of each state are then aggregated and a prediction is made. <br/>


# Installation
## For dockerized environment:
### Install Docker
https://docs.docker.com/get-docker/

### Install Docker Compose
https://docs.docker.com/compose/install/

## For local environment:
### Install Mongodb
https://www.mongodb.com/docs/manual/installation/

### Install Redis
https://redis.io/docs/getting-started/installation/

### Create virtual environment
```
$ python -m venv ./backend/.venv
```
### Activate virtual environment
```
$ . ./backend/.venv/bin/activate
```
### Install python dependencies
```
$ pip install -r ./backend/requirements.txt
```
### Install npm dependencies
```
$ npm --prefix ./frontend install ./frontend
```

# Usage

## For dockerized environment:
### Start containers
```
$ make compose
```
### Start containers with data collections
```
$ make compose-collect
```
## For local environment:
### Start API
```
$ make api
```
### Start UI
```
$ make ui
```
### Start worker
```
$ make worker
```
### Start collecting data:
```
$ make collect
```
