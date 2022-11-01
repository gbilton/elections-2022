# Title

# Table of Contents

# How It Works

# Installation
## For dockerized environment:
Install Docker: docs.docker.com/get-docker/
Install Docker Compose: docs.docker.com/compose/install/

## For local environment:
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
### Install Mongodb
https://www.mongodb.com/docs/manual/installation/

### Install Redis
https://redis.io/docs/getting-started/installation/

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
