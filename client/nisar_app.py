import os
import json
import traceback
import boto3

from unity_on_demand_client import Client
from unity_on_demand_client.api.on_demand_v0_1_0 import create_prewarm_request


print("Loading function")


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    # handle S3 event
    node_count = 0
    if "Records" in event:
        for record in event["Records"]:
            bucket = record["s3"]["bucket"]["name"] 
            obj = record["s3"]["object"]["key"]

            # parse LDF file for number of raw files to prewarm ingest nodes
            s3 = boto3.resource("s3")
            ldf_file_obj = s3.Object(bucket, obj)
            content = ldf_file_obj.get()["Body"].read()
            node_count = len(json.loads(content)["files"])

            # prewarm L0A node
            node_count += 1
    else:
        node_count = event.get("node_count", 1)
    print(f"node_count: {node_count}")

    # build On-Demand client
    if "OD_API_URL" in os.environ:
        url = os.environ["OD_API_URL"]
    else:
        raise RuntimeError("No configured On-Demand API endpoint.")
    client = Client(base_url=url)

    # make prewarm call
    try:
        prewarm_response = create_prewarm_request.sync(
            client=client, node_count=node_count, additive=True
        )
        print(f"prewarm response: {prewarm_response}")
        return prewarm_response.success
    except Exception as e:
        print(e)
        print("Error sending prewarm OD call.")
        print(traceback.format_exc())
        raise e
