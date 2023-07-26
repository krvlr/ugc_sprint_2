sh.addShard("mongors1/mongors1n1");
sh.addShard("mongors2/mongors2n1");

const dbname = "ugc2";
const conn = new Mongo();
const database = conn.getDB(dbname);

sh.enableSharding(dbname);

rating_collection = "rating";
database.createCollection(rating_collection);
sh.shardCollection(`${dbname}.${rating_collection}`, {["user_id"]: "hashed"});
database[rating_collection].createIndex({["film_id"]: -1});
database[rating_collection].createIndex({["rating_score"]: -1});

reviews_collection = "review";
database.createCollection(reviews_collection);
sh.shardCollection(`${dbname}.${reviews_collection}`, {["user_id"]: "hashed"});
database[reviews_collection].createIndex({["film_id"]: -1});

bookmark_collection = "bookmark";
database.createCollection(bookmark_collection);
sh.shardCollection(`${dbname}.${bookmark_collection}`, {["user_id"]: "hashed"});
database[bookmark_collection].createIndex({["film_id"]: -1});

use admin
database.createUser({
  user: "default",
  pwd:  "default_password",
  roles:
      [{ role:"readWrite", db:`${dbname}`}],
  mechanisms: [ "SCRAM-SHA-256" ],
});