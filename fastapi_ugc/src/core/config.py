from pydantic import Field
from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = ".env"


class BaseSettings(BaseConfig):
    project_name: str = Field(default="UGC2", env="PROJECT_NAME")
    secret_key: str = Field(default="SUPER-SECRET-KEY", repr=False, env="JWT_SECRET_KEY")


class MongodbSettings(BaseConfig):
    host: str = Field(default="127.0.0.1", env="MONGODB_HOST")
    port: int = Field(default=27019, env="MONGODB_PORT")
    login: str = Field(default="default", env="MONGODB_LOGIN")
    password: str = Field(default="default_password", env="MONGODB_PASSWORD")
    db_name: str = Field(default="ugc2", env="MONGODB_DB_NAME")
    collection_bookmark: str = Field(default="bookmark", env="MONGODB_COLLECTION_BOOKMARK")


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