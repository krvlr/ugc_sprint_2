import logging
import os
import sys
from asyncio import get_event_loop
from pathlib import Path

import backoff
from motor.motor_asyncio import AsyncIOMotorClient

SCRIPT_DIR = Path(os.path.abspath(__file__))
sys.path.append(os.path.abspath(SCRIPT_DIR.parent.parent.parent.absolute()))

from functional.settings import backoff_settings, mongodbtest_settings

logger = logging.getLogger("Waiting for Mongo")


@backoff.on_exception(**backoff_settings)
async def is_running():
    conn_str = (f"mongodb://{mongodbtest_settings.login}:{mongodbtest_settings.password}@"
                f"{mongodbtest_settings.mongodb_host}:{mongodbtest_settings.mongodb_port}/"
                f"?authSource={mongodbtest_settings.mongo_db_name}&authMechanism=SCRAM-SHA-256")

    client = AsyncIOMotorClient(conn_str, serverSelectionTimeoutMS=5000)
    print(conn_str)
    logger.warning('Waiting for Mongo')
    await client.server_info()


if __name__ == '__main__':
    loop = get_event_loop()
    loop.run_until_complete(is_running())
