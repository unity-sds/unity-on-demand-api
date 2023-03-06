#!/bin/bash
virtualenv env
source env/bin/activate
pip install openapi-python-client
openapi-python-client generate --url http://localhost:8000/openapi.json --config openapi-python-client.yaml
deactivate
rm -rf env
