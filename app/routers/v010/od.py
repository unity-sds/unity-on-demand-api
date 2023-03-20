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
    # TODO: replace this code with a call to the unity-sps-api when it
    # implements prewarm; here we do the prewarming ourselves
    try:
        # initialize EKS client
        client = boto3.client("eks")

        # retrieve EKS cluster name
        if "CLUSTER_NAME" in os.environ:
            cluster_name = os.environ["CLUSTER_NAME"]
        else:
            raise RuntimeError("No configured EKS cluster.")

        # get name of first compute node group
        node_group = client.list_nodegroups(clusterName=cluster_name)["nodegroups"][0]
        logger.info(f"node_group: {node_group}")

        # retrieve info of that node group
        node_group_info = client.describe_nodegroup(
            clusterName=cluster_name, nodegroupName=node_group
        )["nodegroup"]
        logger.info(
            f"node_group_info: {json.dumps(node_group_info, indent=2, cls=DatetimeEncoder)}"
        )

        # increment the desiredSize for the node group by 1
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

        # return update ID
        return {
            "success": True,
            "message": f"Got node_count:{node_count}",
            "request_id": update_resp["update"]["id"],
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        logger.error(f"Got exception: {str(e)}")
        return {"success": False, "message": f"Got exception: {str(e)}"}


@router.get("/prewarm/{request_id}")
async def get_prewarm_request(response: Response, request_id: str) -> PrewarmResponse:
    # TODO: replace this code with a call to the unity-sps-api when it
    # implements getting prewarm status
    try:
        # initialize EKS client
        client = boto3.client("eks")

        # retrieve EKS cluster name
        if "CLUSTER_NAME" in os.environ:
            cluster_name = os.environ["CLUSTER_NAME"]
        else:
            raise RuntimeError("No configured EKS cluster.")

        # get name of first compute node group
        node_group = client.list_nodegroups(clusterName=cluster_name)["nodegroups"][0]
        logger.info(f"node_group: {node_group}")

        # increment the desiredSize for the node group by 1
        update_resp = client.describe_update(
            name=cluster_name, nodegroupName=node_group, updateId=request_id
        )
        logger.info(
            f"update_resp: {json.dumps(update_resp, indent=2, cls=DatetimeEncoder)}"
        )

        # return update status
        status = update_resp["update"]["status"]
        return {
            "success": True,
            "message": f"Prewarm status for EKS update ID {request_id}: {status}",
            "request_id": request_id,
        }
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        logger.error(f"Got exception: {str(e)}")
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
