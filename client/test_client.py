#!/usr/bin/env python
from unity_on_demand_client import Client
from unity_on_demand_client.api.test import echo
from unity_on_demand_client.api.on_demand_v0_1_0 import create_prewarm_request, get_prewarm_request, cancel_prewarm_request


# test echo
client = Client(base_url="http://localhost:8000")
t = echo.sync(client=client, echo_str="test this")
print(t)

# test creation of prewarm request
p = create_prewarm_request.sync(client=client)
print(p)

# test getting status of prewarm request
s = get_prewarm_request.sync(client=client, request_id=p.request_id)
print(s)

# test cancellation of prewarm request
c = cancel_prewarm_request.sync(client=client, request_id=p.request_id)
print(c)
