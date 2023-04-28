import os
import json

from unity_on_demand_client import Client
from unity_on_demand_client.api.on_demand_v0_1_0 import create_prewarm_request


print("Loading function")


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    # build On-Demand client
    if "OD_API_URL" in os.environ:
        url = os.environ["OD_API_URL"]
    else:
        raise RuntimeError("No configured On-Demand API endpoint.")
    client = Client(base_url=url)

    # make prewarm call
    try:
        prewarm_response = create_prewarm_request.sync(
            client=client, node_count=1, additive=True
        )
        print(f"prewarm response: {prewarm_response}")
        return prewarm_response.success
    except Exception as e:
        print(e)
        print("Error sending prewarm OD call.")
        raise e
