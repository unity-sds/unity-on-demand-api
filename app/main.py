import os
import logging
import logging.config
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from mangum import Mangum

from .config import Settings, get_settings
from .routers import test
from .routers.v010 import od as od_v010
from .routers.v020 import od as od_v020


# setup loggers
logging.config.fileConfig(
    os.path.join(os.path.dirname(__file__), "..", "logging.conf"),
    disable_existing_loggers=False,
)

# get root logger
logger = logging.getLogger(__name__)


app = FastAPI(
    title="Unity On-Demand REST API",
    version="0.0.2",
    description="Unity On-Demand Operations",
    root_path=f"/{os.environ.get('STAGE')}/" if "STAGE" in os.environ else None,
    generate_unique_id_function=lambda route: f"{route.name}",
)


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root(settings: Settings = Depends(get_settings)):
    return {"message": f"Hello from the On-Demand REST API at stage {settings.stage}!"}


app.include_router(od_v010.router)
app.include_router(od_v020.router)
app.include_router(test.router)

handler = Mangum(app)
