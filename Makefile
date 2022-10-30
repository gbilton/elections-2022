api:
	uvicorn main:app --reload

worker:
	rq worker

collect:
	python collect.py

prune: 
	docker system prune -a

compose:
	docker-compose up -d --build

down:
	docker-compose down