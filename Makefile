.PHONY: docker-run
docker-run: ./makeLog/compose_build.log
	docker-compose up

./makeLog/compose_build.log : requirements.txt makeLog
	docker-compose build > ./makeLog/compose_build.log

makeLog:
	mkdir makeLog