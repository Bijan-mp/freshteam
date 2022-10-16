build:
	docker build -t freshteam .


test: 
	docker run -it freshteam sh test.sh

run-dev:
	docker compose up -d

run-prod:
	docker swarm init
	docker stack deploy --compose-file docker-compose.yml freshteam

createsuperuser:
	docker compose exec backend python3 /app/src/manage.py createsuperuser
	
scale-service:
	docker service scale freshteam_backend=$(replica-num)
