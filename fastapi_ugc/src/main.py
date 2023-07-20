import uvicorn

from api.v1 import core, ugc2
from core.config import base_settings, logger_settings
from core.logger import LOGGER_CONFIG
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title=base_settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    pass


@app.on_event("shutdown")
async def shutdown():
    pass


# app.include_router(, prefix="/api/v1/", tags=[""])
app.include_router(core.router, prefix="/api/v1", tags=["core"])
app.include_router(ugc2.router, prefix="/api/v1/ugc2", tags=["ugc2"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=LOGGER_CONFIG,
        debug=logger_settings.debug,
    )
