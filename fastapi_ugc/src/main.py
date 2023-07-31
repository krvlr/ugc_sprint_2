import logging
import sentry_sdk
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from api.v1 import core, ratings, bookmarks, reviews
from core.config import base_settings, mongodb_settings
from core.logger import LOGGING_CONFIG
from db import mongodb_adapter

from core.logstash import config_logstash, add_log_request_id


app = FastAPI(
    title=base_settings.project_name,
    docs_url="/api/v1/ugc2/openapi",
    openapi_url="/api/v1/ugc2/openapi.json",
    default_response_class=ORJSONResponse,
)

logger = logging.getLogger(__name__)


if base_settings.sentry_dsn:
    sentry_sdk.init(
        dsn=base_settings.sentry_dsn,
        traces_sample_rate=1.0,
    )


@app.middleware("http")
async def log_middle(request: Request, call_next):
    request_id = request.headers.get("X-Request-Id")
    add_log_request_id(request_id)
    response = await call_next(request)
    return response


@app.on_event("startup")
async def startup():
    mongodb_adapter.client = AsyncIOMotorClient(
        f"mongodb://{mongodb_settings.login}:{mongodb_settings.password}@"
        f"{mongodb_settings.mongodb_host}:{mongodb_settings.mongodb_port}/"
        f"?authSource={mongodb_settings.mongo_db_name}&authMechanism=SCRAM-SHA-256"
    )
    config_logstash()


@app.on_event("shutdown")
async def shutdown():
    await mongodb_adapter.client.close()


app.include_router(core.router, prefix="/api/v1/ugc2", tags=["core"])
app.include_router(bookmarks.router, prefix="/api/v1/ugc2/bookmarks", tags=["bookmarks"])
app.include_router(ratings.router, prefix="/api/v1/ugc2/ratings", tags=["ratings"])
app.include_router(reviews.router, prefix="/api/v1/ugc2/reviews", tags=["reviews"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_config=LOGGING_CONFIG)
