import os
import logging
import json
import traceback
from typing import Optional

from fastapi import APIRouter, Response, status
from pydantic import BaseModel
import httpx

from ...utils import DatetimeEncoder


logger = logging.getLogger(__name__)

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
    request_id: Optional[str]


@router.post("/prewarm")
async def create_prewarm_request(
    response: Response, node_count: int = 20
) -> PrewarmResponse:
    try:
        # retrieve EKS cluster name
        if "CLUSTER_NAME" in os.environ:
            cluster_name = os.environ["CLUSTER_NAME"]
        else:
            raise RuntimeError("No configured EKS cluster.")

        # retrieve SPS API URL
        if "SPS_API_URL" in os.environ:
            sps_api_url = os.environ["SPS_API_URL"]
        else:
            raise RuntimeError("No configured SPS API URL.")

        # retrieve info of that node group
        r = httpx.get(f"{sps_api_url}/sps/node-group-info")
        r.raise_for_status()
        node_group_info = r.json()
        logger.info(
            f"node_group_info: {json.dumps(node_group_info, indent=2, cls=DatetimeEncoder)}"
        )

        # increment the desiredSize for the node group by 1
        r = httpx.post(f"{sps_api_url}/sps/prewarm", json={"num_nodes": node_group_info["desired_size"] + 1})
        r.raise_for_status()
        update_resp = r.json()
        logger.info(
            f"update_resp: {json.dumps(update_resp, indent=2, cls=DatetimeEncoder)}"
        )

        # return update ID
        return {
            "success": True,
            "message": f"Got node_count:{node_count}",
            "request_id": update_resp["prewarm_request_id"],
        }
    except Exception as e:
        logger.error(f"Got exception: {str(e)}")
        logger.error(traceback.format_exc())
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"success": False, "message": f"Got exception: {str(e)}"}


@router.get("/prewarm/{request_id}")
async def get_prewarm_request(response: Response, request_id: str) -> PrewarmResponse:
    try:
        # retrieve EKS cluster name
        if "CLUSTER_NAME" in os.environ:
            cluster_name = os.environ["CLUSTER_NAME"]
        else:
            raise RuntimeError("No configured EKS cluster.")

        # retrieve SPS API URL
        if "SPS_API_URL" in os.environ:
            sps_api_url = os.environ["SPS_API_URL"]
        else:
            raise RuntimeError("No configured SPS API URL.")

        # retrieve info on prewarm request ID
        r = httpx.get(f"{sps_api_url}/sps/prewarm/{request_id}")
        r.raise_for_status()
        status_resp = r.json()
        logger.info(
            f"status_resp: {json.dumps(status_resp, indent=2, cls=DatetimeEncoder)}"
        )

        # return status
        status = status_resp["status"]
        return {
            "success": True,
            "message": f"Prewarm status for EKS update ID {request_id}: {status}",
            "request_id": request_id,
        }
    except Exception as e:
        logger.error(f"Got exception: {str(e)}")
        logger.error(traceback.format_exc())
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"success": False, "message": f"Got exception: {str(e)}"}


@router.delete("/prewarm/{request_id}")
async def cancel_prewarm_request(
    response: Response, request_id: str
) -> PrewarmResponse:
    return {
        "success": True,
        "message": f"Submitted cancellation of prewarm request ID {request_id}",
        "request_id": request_id,
    }