SHELL = /bin/sh
CURRENT_UID := $(shell id -u)

mongo_setup_cluster:
	docker exec -it mongocfg1 bash -c "cat /scripts/init_mongocfg1.js | mongosh"
	docker exec -it mongors1n1 bash -c "cat /scripts/init_mongors1n1.js | mongosh"
	docker exec -it mongors2n1 bash -c "cat /scripts/init_mongors2n1.js | mongosh"
	sleep 20
	docker exec -it mongos1 bash -c "cat /scripts/init_mongos1.js | mongosh"