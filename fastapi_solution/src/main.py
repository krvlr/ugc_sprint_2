import uvicorn
from api.v1 import films, genres, persons, core
from core import config
from core.config import (
    jaeger_settings,
    base_settings,
    logger_settings,
    redis_settings,
    elastic_settings,
)
from core.logger import LOGGER_CONFIG
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis

from utils.jaeger_config import configure_jaeger_tracer

from db import elastic, redis

app = FastAPI(
    title=base_settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

configure_jaeger_tracer(app, jaeger_settings.host, jaeger_settings.port)


@app.on_event("startup")
async def startup():
    redis.redis = Redis(host=redis_settings.host, port=redis_settings.port)
    elastic.es = AsyncElasticsearch(hosts=[f"{elastic_settings.host}:{elastic_settings.port}"])


@app.on_event("shutdown")
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


app.include_router(films.router, prefix="/api/v1/films", tags=["films"])
app.include_router(genres.router, prefix="/api/v1/genres", tags=["genres"])
app.include_router(persons.router, prefix="/api/v1/persons", tags=["persons"])
app.include_router(core.router, prefix="/api/v1", tags=["core"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGER_CONFIG,
        debug=logger_settings.debug,
    )
