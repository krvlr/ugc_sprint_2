import logging.config

from core.config import base_settings

from utils.extract import KafkaExtractor, Extractor
from utils.transform import DataTransformer, Transformer
from utils.load import ClickHouseLoader, Loader

from clickhouse_driver import Client
from confluent_kafka.cimpl import Consumer

from core.logger import LOGGER_CONFIG

logging.config.dictConfig(LOGGER_CONFIG)
logger = logging.getLogger(__name__)


def etl(extrator: Extractor, transformer: Transformer, loader: Loader):
    """Основной метод перекачки данных из Kafka в ClickHouse."""
    logger.info("Start etl from Kafka to ClickHouse")
    events = extrator.get_batch_extractor(
        batch_size=int(base_settings.num_messages), timeout=int(base_settings.timeout)
    )
    transform_events = transformer.get_batch_transformer(events)
    loader.save_data(transform_events)


def main():
    logger.info("Start main")

    kafka_extractor = KafkaExtractor(
        consumer=Consumer(base_settings.get_kafka_config()),
        topics=base_settings.get_kafka_topics(),
    )
    data_transformer = DataTransformer()
    click_house_loader = ClickHouseLoader(
        client=Client(
            host=base_settings.clickhouse_host,
            alt_hosts=base_settings.clickhouse_alt_hosts,
            password=base_settings.clickhouse_password,
        )
    )

    while True:
        try:
            etl(extrator=kafka_extractor, transformer=data_transformer, loader=click_house_loader)
        except Exception as ex:
            logger.error(f"Error etl data from Kafka to ClickHouse: {ex}")


if __name__ == "__main__":
    main()
