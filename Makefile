.PHONY: behave-wip
behave-wip:
	docker exec -it behave behave -k --tags @wip

.PHONY: behave
behave:
	docker exec -it behave behave

.PHONY: docker-status
docker-status:
	docker ps --format "{{.Status}}" -af name=behave

.PHONY: docker-stop
docker-stop:
	docker-compose stop

.PHONY: docker-run
docker-run: ./dockerFiles/logs/compose_build.log
	docker-compose up -d

./dockerFiles/logs/compose_build.log : ./dockerFiles/python/requirements.txt \
									   ./dockerFiles/python/Dockerfile
	mkdir -p ./dockerFiles/logs
	docker-compose build > ./dockerFiles/logs/compose_build.log

./dockerFiles/python/requirements.txt: conf/python/requirements.txt
	echo '#Generated file do not edit'  \
	| cat - ./conf/python/requirements.txt > ./dockerFiles/python/requirements.txt
