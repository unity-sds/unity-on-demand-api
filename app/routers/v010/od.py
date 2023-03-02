from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/on-demand/v010",
    tags=["on-demand v0.1.0"],
    responses={
        200: {"description": "Success"},
        400: {"description": "Invalid parameters"},
        401: {"description": "Unauthorized"},
        500: {"description": "Execution failed"},
        501: {"description": "Not implemented"},
    },
)


class PrewarmResponse(BaseModel):
    success: bool
    message: str
    request_id: str


@router.post("/prewarm")
async def create_prewarm_request(node_count: int = 20) -> PrewarmResponse:
    return {
        "success": True,
        "message": f"Got node_count:{node_count}",
        "request_id": "some-request-id",
    }


@router.get("/prewarm/{request_id}")
async def get_prewarm_request(request_id: str) -> PrewarmResponse:
    return {
        "success": True,
        "message": f"Status for prewarm request ID {request_id}",
        "request_id": request_id,
    }


@router.delete("/prewarm/{request_id}")
async def cancel_prewarm_request(request_id: str) -> PrewarmResponse:
    return {
        "success": True,
        "message": f"Submitted cancellation of prewarm request ID {request_id}",
        "request_id": request_id,
    }
