prune: 
	docker system prune -a

compose:
	docker-compose up -d --build

compose-collect:
	docker-compose --profile collect up -d --build

down:
	docker-compose down


# backend

api:
	uvicorn app.asgi:app --reload --app-dir ./backend

worker:
	rq worker

collect:
	python backend/app/collector.py


# frontend

ui:
	npm --prefix ./frontend start

install:
	npm --prefix ./frontend install ./frontend