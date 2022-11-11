from typing import Any

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from src.building_blocks.errors import APIErrorMessage, DomainError, RepositoryError, ResourceNotFound
from src.clients.controllers import router as clients_router
from src.gym_classes.controllers import router as gym_classes_router
from src.gym_passes.controllers import router as gym_passes_router

app = FastAPI()
app.include_router(gym_classes_router)
app.include_router(clients_router)
app.include_router(gym_passes_router)


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    error_msg = APIErrorMessage(type=exc.__class__.__name__, message=f"Oops! {exc}")
    return JSONResponse(
        status_code=400,
        content=error_msg.dict(),
    )


@app.exception_handler(ResourceNotFound)
async def resource_not_found_handler(request: Request, exc: ResourceNotFound) -> JSONResponse:
    error_msg = APIErrorMessage(type=exc.__class__.__name__, message=str(exc))
    return JSONResponse(status_code=404, content=error_msg.dict())


@app.exception_handler(RepositoryError)
async def repository_error_handler(request: Request, exc: RepositoryError) -> JSONResponse:
    error_msg = APIErrorMessage(
        type=exc.__class__.__name__, message="Oops! Something went wrong, please try again later..."
    )
    return JSONResponse(
        status_code=500,
        content=error_msg.dict(),
    )


def custom_openapi() -> dict[str, Any]:
    if app.openapi_schema:
        return app.openapi_schema  # type: ignore

    openapi_schema = get_openapi(
        title="hexagonal-architecture-python",
        version="1.0.0",
        description="Hexagonal architecture in Python build on top of FastAPI",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema

    return app.openapi_schema  # type: ignore


app.openapi = custom_openapi  # type: ignore

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
