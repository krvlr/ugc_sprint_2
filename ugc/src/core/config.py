import logging
import os

from pydantic import BaseSettings, Field


class BaseConfig(BaseSettings):
    class Config:
        env_file = ".env"


class BaseSettings(BaseConfig):
    project_name: str = Field(default="movies", env="PROJECT_NAME")


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


class KafkaSettings(BaseConfig):
    host: str = Field(default="127.0.0.1", env="KAFKA_HOST")
    port: str = Field(default="9092", env="KAFKA_PORT")
    topic: str = Field(default="movies_views", env="KAFKA_TOPICS")


base_settings = BaseSettings()
logger_settings = LoggerSettings()
jaeger_settings = JaegerSettings()
kafka_settings = KafkaSettings()
