from fastapi import Depends, FastAPI
from fastapi.openapi.utils import get_openapi
from mangum import Mangum

from .routers import test, od

app = FastAPI()


app.include_router(od.router)
app.include_router(test.router)


@app.get("/")
async def root():
    return {"message": "Hello from the On-Demand REST API!"}


def custom_openapi():
    """Customize the OpenAPI page."""

    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Unity On-Demand REST API",
        version="0.0.1",
        description="Unity On-Demand Operations",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

handler = Mangum(app)
