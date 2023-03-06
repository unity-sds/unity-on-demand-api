#!/bin/bash
virtualenv env
source env/bin/activate
pip install pytest
pip install -e unity-on-demand-api-client
pytest -s --log-cli-level=INFO test_client.py
deactivate
rm -rf env
