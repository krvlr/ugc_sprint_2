docker-compose exec mongocfg1 sh -c "mongosh < /scripts/init_mongocfg1.js"
docker-compose exec mongors1n1 sh -c "mongosh < /scripts/init_mongors1n1.js"
docker-compose exec mongors2n1 sh -c "mongosh  < /scripts/init_mongors2n1.js"

timeout 10

docker-compose exec mongos1 sh -c "mongosh < /scripts/init_mongos1.js"


timeout 10
