from flask import Blueprint
from flask_restx import Api


services = Blueprint('api_v0-1', __name__, url_prefix='/api/v0.1')
api = Api(services, ui=False, version="0.1", title="On-Demand REST API",
          description="REST API for On-Demand.")


# namespaces
test_ns = api.namespace('test', description="test operations")
od_ns = api.namespace('od', description="od operations")
