from pydantic import Field
from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = ".env"


class BaseSettings(BaseConfig):
    project_name: str = Field(default="ugc", env="PROJECT_NAME")


class MongodbSettings(BaseConfig):
    host: str = Field(default="127.0.0.1", env="MONGODB_HOST")
    port: int = Field(default=27017, env="MONGODB_PORT")
    login: str = Field(default="", env="MONGODB_LOGIN")
    password: str = Field(default="", env="MONGODB_PASSWORD")
    db_name: str = Field(default="ugc2", env="MONGODB_DB_NAME")


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
