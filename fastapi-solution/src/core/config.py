import logging
import os

from pydantic import BaseSettings, Field


class BaseConfig(BaseSettings):
    class Config:
        env_file = ".env"


class BaseSettings(BaseConfig):
    project_name: str = Field(default="movies", env="PROJECT_NAME")
    secret_key: str = Field(default="SUPER-SECRET-KEY", env="JWT_SECRET_KEY")
    cache_expire_in_seconds: int = Field(default=60, env="CACHE_EXPIRE_SEC")


class RedisSettings(BaseConfig):
    host: str = Field(default="127.0.0.1", env="REDIS_HOST")
    port: int = Field(default=6379, env="REDIS_PORT")


class ElasticSettings(BaseConfig):
    host: str = Field(default="127.0.0.1", env="ELASTIC_HOST")
    port: str = Field(default=9200, env="ELASTIC_PORT")


class LoggerSettings(BaseConfig):
    debug: str = Field(default="True", env="DEBUG")
    level: str = Field(default="INFO", env="LOGGING_LEVEL")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOG_FORMAT"
    )
    default_handlers: list = ["console"]


class JaegerSettings(BaseConfig):
    enable_tracer: bool = Field(default=True, env="ENABLE_TRACER")
    host: str = Field(default="127.0.0.1", env="JAEGER_HOST")
    port: int = Field(default=6831, env="JAEGER_PORT")


base_settings = BaseSettings()
redis_settings = RedisSettings()
elastic_settings = ElasticSettings()
logger_settings = LoggerSettings()
jaeger_settings = JaegerSettings()
