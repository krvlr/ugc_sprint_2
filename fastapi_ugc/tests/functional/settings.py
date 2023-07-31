import logging
import backoff
from pydantic import Field
from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    elastic_host: str = Field(default="elasticsearchelk", env="ELASTIC_HOST")
    elastic_port: str = Field(default=9200, env="ELASTIC_PORT")
    redis_host: str = Field(default="redis", env="REDIS_HOST")
    redis_port: int = Field(default=6379, env="REDIS_PORT")
    api_url: str = Field(default="http://api:8000/api/v1", evn="API_URL")

    class Config:
        env_file = ".env"


class MongodbSettingsTest(BaseSettings):
    mongodb_host: str = Field(default="mongos1", env="MONGODB_HOST")
    mongodb_port: int = Field(default=27017, env="MONGODB_PORT")
    login: str = Field(default="default", env="MONGODB_LOGIN")
    password: str = Field(default="default_password", env="MONGODB_PASSWORD")
    mongo_db_name: str = Field(default="ugc2", env="MONGODB_DB_NAME")
    collection_bookmark: str = Field(default="bookmark", env="MONGODB_COLLECTION_BOOKMARK")
    collection_review: str = Field(default="review", env="MONGODB_COLLECTION_REVIEW")
    collection_rating: str = Field(default="rating", env="MONGODB_COLLECTION_RATING")

    class Config:
        env_file = ".env"


def backoff_hdlr(details):
    logging.warning("Backing off {wait:0.1f} seconds after {tries} tries "
                    "calling function {target} with args {args} and kwargs "
                    "{kwargs}".format(**details))


backoff_settings = {
    "wait_gen": backoff.expo,
    "exception": Exception,
    "max_tries": 20,
    'max_time': 30,
    'jitter': None,
    'on_backoff': backoff_hdlr
}

test_settings = TestSettings()
mongodbtest_settings = MongodbSettingsTest()
