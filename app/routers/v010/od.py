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


def get_conf():
    """Retrieve configuration parameters through environment variables."""

    # configuration dict
    conf = dict()

    # retrieve EKS cluster name
    if "CLUSTER_NAME" in os.environ:
        conf["cluster_name"] = os.environ["CLUSTER_NAME"]
    else:
        raise RuntimeError("No configured EKS cluster.")

    # retrieve SPS API URL
    if "SPS_API_URL" in os.environ:
        conf["sps_api_url"] = os.environ["SPS_API_URL"]
    else:
        raise RuntimeError("No configured SPS API URL.")

    # log conf
    logger.info(f"conf: {conf}")

    return conf


@router.post("/prewarm")
async def create_prewarm_request(
    response: Response, node_count: int = 1, additive: bool = False
) -> PrewarmResponse:
    try:
        # retrieve conf
        conf = get_conf()

        # retrieve info of that node group
        r = httpx.get(f"{conf['sps_api_url']}/sps/node-group-info")
        r.raise_for_status()
        node_group_info = r.json()
        logger.info(
            f"node_group_info: {json.dumps(node_group_info, indent=2, cls=DatetimeEncoder)}"
        )

        # node_count is absolute or additive?
        desired_size = node_group_info["desired_size"]
        prewarm_count = desired_size + node_count if additive else node_count
        logger.info(
            f"additive, prewarm_count: {additive}, {prewarm_count}"
        )

        # call prewarm only if there are nodes to add (don't terminated nodes)
        if prewarm_count <= desired_size:
            return {
                "success": True,
                "message": f"Not need to prewarm. {desired_size} nodes are already desired.",
                "request_id": ""
            }


        # prewarm to node_count passed in
        r = httpx.post(f"{conf['sps_api_url']}/sps/prewarm", json={"num_nodes": prewarm_count})
        r.raise_for_status()
        update_resp = r.json()
        logger.info(
            f"update_resp: {json.dumps(update_resp, indent=2, cls=DatetimeEncoder)}"
        )

        # return update ID
        return {
            "success": True,
            "message": f"Prewarming to node count: {prewarm_count}",
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
        # retrieve conf
        conf = get_conf()

        # retrieve info on prewarm request ID
        r = httpx.get(f"{conf['sps_api_url']}/sps/prewarm/{request_id}")
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