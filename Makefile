prune: 
	docker system prune -a

compose:
	docker-compose up -d --build

collect:
	docker-compose --profile collect up -d --build

down:
	docker-compose down

