#!/bin/bash
virtualenv env
source env/bin/activate
pip install openapi-python-client
if [ -d "unity-on-demand-api-client" ]; then
  action=update
else
  action=generate
fi
openapi-python-client $action --url http://localhost:8000/openapi.json --config openapi-python-client.yaml
deactivate
rm -rf env
