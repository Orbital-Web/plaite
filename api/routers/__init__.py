from contextlib import asynccontextmanager

from fastapi import FastAPI
from schemas import HealthCheck

from routers.foodcv import router as cv_router
from routers.foodstats import router as stats_router

tags = [
    {"name": "FoodCV", "description": "Endpoints for food recognition"},
    {"name": "FoodStats", "description": "Endpoints for food stats retrieval"},
    {"name": "healthcheck", "description": "Endpoint for performing health checks"},
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    app.var = 5  # you can attach variables to the app to use later
    yield
    # shutdown
    # clean up resources here


app = FastAPI(lifespan=lifespan, openapi_tags=tags)
app.include_router(cv_router, prefix="/foodcv", tags=["FoodCV"])
app.include_router(stats_router, prefix="/foodstats", tags=["FoodStats"])


@app.get("/health", tags=["healthcheck"])
async def perform_healthcheck() -> HealthCheck:
    return HealthCheck(status="OK")
