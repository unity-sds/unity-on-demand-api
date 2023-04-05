import logging

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.config import Settings, get_settings


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/test",
    tags=["test"],
    responses={
        200: {"description": "Success"},
        400: {"description": "Invalid parameters"},
        401: {"description": "Unauthorized"},
        500: {"description": "Echo execution failed"},
    },
)


class EchoResponse(BaseModel):
    success: bool
    message: str


@router.get("/echo")
async def echo(
    echo_str: str, settings: Settings = Depends(get_settings)
) -> EchoResponse:
    logger.info("logging from app logger")
    return {
        "success": True,
        "message": f"Echoing '{echo_str}' from stage {settings.stage}",
    }
