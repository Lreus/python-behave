.PHONY: behave-wip
behave-wip:
	docker exec -it behave behave --tags @wip

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

./makeLog/compose_build.log : ./DockerFiles/python/requirements.txt \
 							  DockerFiles/python/Dockerfile \
 							  makeLog
	docker-compose build > ./makeLog/compose_build.log

./DockerFiles/python/requirements.txt: requirements.txt
	echo '#Generated file do not edit' | cat - ./requirements.txt > ./DockerFiles/python/requirements.txt

makeLog:
	mkdir makeLog