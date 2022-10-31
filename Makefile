prune: 
	docker system prune -a

compose:
	docker-compose up -d --build

down:
	docker-compose down