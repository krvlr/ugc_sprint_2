import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from api.v1 import core, ratings, bookmarks, reviews
from core.config import base_settings, mongodb_settings
from core.logger import LOGGER_CONFIG
from db import mongodb_adapter

app = FastAPI(
    title=base_settings.project_name,
    docs_url="/api/v1/ugc2/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    mongodb_adapter.client = AsyncIOMotorClient(
        f"mongodb://{mongodb_settings.login}:{mongodb_settings.password}@"
        f"{mongodb_settings.mongodb_host}:{mongodb_settings.mongodb_port}/"
        f"?authSource={mongodb_settings.mongo_db_name}&authMechanism=SCRAM-SHA-256"
    )


@app.on_event("shutdown")
async def shutdown():
    await mongodb_adapter.client.close()


app.include_router(core.router, prefix="/api/v1/ugc2", tags=["core"])
app.include_router(bookmarks.router, prefix="/api/v1/ugc2/bookmarks", tags=["bookmarks"])
app.include_router(ratings.router, prefix="/api/v1/ugc2/ratings", tags=["ratings"])
app.include_router(reviews.router, prefix="/api/v1/ugc2/reviews", tags=["reviews"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_config=LOGGER_CONFIG)
