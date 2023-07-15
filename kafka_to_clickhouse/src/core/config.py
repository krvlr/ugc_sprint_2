from pydantic import BaseSettings, Field


class BaseConfig(BaseSettings):
    class Config:
        env_file = ".env"


class BaseSettings(BaseConfig):
    kafka_host: str = Field("127.0.0.1", env="KAFKA_HOST")
    kafka_port: str = Field(default="9092", env="KAFKA_PORT")
    clickhouse_host: str = Field(default="127.0.0.1", env="CLICKHOUSE_HOST")
    clickhouse_alt_hosts: str = Field(
        default="clickhouse-node2, clickhouse-node3, clickhouse-node4", env="CLICKHOUSE_ALT_HOSTS"
    )
    clickhouse_password = Field(default="default_password", env="CLICKHOUSE_PASSWORD")
    topics: str = Field(default="movies_views", env="KAFKA_TOPICS")
    num_messages: str = Field(default="200", env="KAFKA_EXTRACT_NUM_MESSAGES")
    timeout: str = Field(default="10", env="KAFKA_EXTRACT_TIMEOUT")
    group_id: str = Field(default="app", env="KAFKA_GROUP_ID")
    auto_offset_reset: str = Field(default="smallest", env="KAFKA_AUTO_OFFSET_RESET")

    def get_kafka_topics(self):
        return self.topics.split(", ")

    def get_kafka_config(self) -> dict:
        return {
            "bootstrap.servers": f"{self.kafka_host}:{self.kafka_port}",
            "group.id": self.group_id,
            "auto.offset.reset": self.auto_offset_reset,
        }


class LoggerSettings(BaseConfig):
    level: str = Field(default="INFO", env="LOGGING_LEVEL")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOG_FORMAT"
    )
    default_handlers: list = ["console"]


base_settings = BaseSettings()
logger_settings = LoggerSettings()
