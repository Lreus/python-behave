.PHONY: behave
behave:
	docker exec -it behave behave

.PHONY: docker-status
docker-status:
	docker ps --format "{{.Status}}" -af name=behave

.PHONY: docker-stop
docker-stop:
	docker stop behave

.PHONY: docker-run
docker-run: ./makeLog/compose_build.log
	docker-compose up -d

./makeLog/compose_build.log : requirements.txt Dockerfile makeLog
	docker-compose build > ./makeLog/compose_build.log

makeLog:
	mkdir makeLog