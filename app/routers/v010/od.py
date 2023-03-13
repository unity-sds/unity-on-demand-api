import os
import logging
import json
from typing import Optional

from fastapi import APIRouter, Response, status
from pydantic import BaseModel
import boto3

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
        client = boto3.client("eks")
        # clusters = client.list_clusters()
        # logger.info(f"clusters: {json.dumps(clusters, indent=2)}")
        if "CLUSTER_NAME" in os.environ:
            cluster_name = os.environ["CLUSTER_NAME"]
        else:
            raise RuntimeError("No configured EKS cluster.")
        node_group = client.list_nodegroups(clusterName=cluster_name)["nodegroups"][0]
        logger.info(f"node_group: {node_group}")
        node_group_info = client.describe_nodegroup(
            clusterName=cluster_name, nodegroupName=node_group
        )["nodegroup"]
        logger.info(
            f"node_group_info: {json.dumps(node_group_info, indent=2, cls=DatetimeEncoder)}"
        )
        update_resp = client.update_nodegroup_config(
            clusterName=cluster_name,
            nodegroupName=node_group,
            scalingConfig={
                "desiredSize": node_group_info["scalingConfig"]["desiredSize"] + 1
            },
        )
        logger.info(
            f"update_resp: {json.dumps(update_resp, indent=2, cls=DatetimeEncoder)}"
        )
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"success": False, "message": f"Got exception: {str(e)}"}
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
