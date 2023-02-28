from builtins import str, bool, float

import traceback
from flask import current_app, request
from flask_restx import Resource, fields

from unity_on_demand.controllers.api_v01.config import api, od_ns


@od_ns.route("/od/data/prewarm", endpoint="prewarm")
@api.doc(
    responses={
        200: "Success",
        400: "Invalid parameters",
        401: "Unathorized",
        500: "Execution failed",
    },
    description="Prewarm SPS.",
)
class Prewarm(Resource):
    """Pre-warm SPS."""

    arg_parser = od_ns.parser()
    arg_parser.add_argument(
        "request_id", type=str, help="prewarm request ID", required=True
    )

    json_parser = od_ns.parser()
    json_parser.add_argument(
        "gpu_needed", location="json", type=bool, help="Need GPU?", required=False
    )
    json_parser.add_argument(
        "disk_space_in_gb",
        location="json",
        type=int,
        help="Disk space needed in GB",
        required=False,
    )
    json_parser.add_argument(
        "mem_size_in_gb",
        location="json",
        type=int,
        help="Memory size needed in GB",
        required=False,
    )

    model = api.model(
        "Prewarm",
        {
            "success": fields.Boolean(description="success flag"),
            "message": fields.String(description="message"),
            "request_id": fields.String(description="prewarm request ID"),
        },
    )

    @od_ns.expect(arg_parser)
    @api.marshal_with(model)
    @api.doc(security="apikey")
    def get(self):
        try:
            request_id = request.args.get("request_id")
            return {
                "success": True,
                "message": f"Status for prewarm request ID {request_id}",
                "request_id": request_id,
            }
        except Exception as e:
            return {"success": False, "message": str(e)}, 400

    @od_ns.expect(json_parser)
    @api.marshal_with(model)
    @api.doc(security="apikey")
    def post(self):
        request_json = request.get_json()
        gpu = request_json.get("gpu_needed", False)
        disk_space_in_gb = request_json.get("disk_space_in_gb", 20)
        mem_size_in_gb = request_json.get("mem_size_in_gb", 4)

        try:
            return {
                "success": True,
                "message": f"Got gpu_needed:{gpu}, disk_space_in_gb: {disk_space_in_gb}, mem_size_in_gb: {mem_size_in_gb}",
                "request_id": "some-request-id",
            }
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
            return {
                "success": False,
                "message": str(e),
            }, 500
