#!/bin/bash
virtualenv env
source env/bin/activate
pip install -e unity-on-demand-api-client
python test_client.py
deactivate
rm -rf env
