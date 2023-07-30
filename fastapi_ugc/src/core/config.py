from pydantic import Field
from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = ".env"


class BaseSettings(BaseConfig):
    project_name: str = Field(default="UGC2", env="PROJECT_NAME")
    secret_key: str = Field(default="SUPER-SECRET-KEY", repr=False, env="JWT_SECRET_KEY")
    sentry_dsn: str = Field(default="123", env="SENTRY_DSN")
    logstash_host: str = Field(default="logstashelk", env="LOGSTASH_HOST")
    logstash_port: int = Field(default=5044, env="LOGSTASH_PORT")


class MongodbSettings(BaseConfig):
    mongodb_host: str = Field(default="mongos1", env="MONGODB_HOST")
    mongodb_port: int = Field(default=27017, env="MONGODB_PORT")
    login: str = Field(default="default", env="MONGODB_LOGIN")
    password: str = Field(default="default_password", env="MONGODB_PASSWORD")
    mongo_db_name: str = Field(default="ugc2", env="MONGODB_DB_NAME")
    collection_bookmark: str = Field(default="bookmark", env="MONGODB_COLLECTION_BOOKMARK")
    collection_review: str = Field(default="review", env="MONGODB_COLLECTION_REVIEW")
    collection_rating: str = Field(default="rating", env="MONGODB_COLLECTION_RATING")


class LoggerSettings(BaseConfig):
    debug: str = Field(default="True", env="DEBUG")
    level: str = Field(default="INFO", env="LOGGING_LEVEL")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOG_FORMAT"
    )
    default_handlers: list = ["console"]


base_settings = BaseSettings()
mongodb_settings = MongodbSettings()
logger_settings = LoggerSettings()
