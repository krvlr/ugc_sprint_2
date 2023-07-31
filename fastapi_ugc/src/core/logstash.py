import logging
from logstash_async.handler import AsynchronousLogstashHandler, LogstashFormatter

from core.config import base_settings


logger = logging.getLogger("")


def config_logstash():
    formatter = LogstashFormatter(
        tags=[
            "events_ugc",
        ]
    )
    handler = AsynchronousLogstashHandler(
        base_settings.logstash_host,
        base_settings.logstash_port,
        transport="logstash_async.transport.UdpTransport",
        database_path="logstash.db",
    )
    handler.formatter = formatter
    logger.addHandler(handler)


def add_log_request_id(request_id: str | None):
    logger.info(f"request_id {request_id}")
