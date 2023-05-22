#!/bin/bash
set -ex

# install serverless
npm install -g serverless

# print serverless version
serverless --version

# clone unity-on-demand-api repo
git clone https://github.com/unity-sds/unity-on-demand-api.git

# deploy
cd unity-on-demand-api
serverless plugin install -n serverless-python-requirements
serverless plugin install -n serverless-wsgi
#serverless deploy --param cluster_name=unity-sps-on-demand-${RandomStringResource.RandomString} \
#                                        --param sps_api_url=http://${!sps_api}:5002 \
#                                        --param permissionsBoundaryPolicyName=${PrivilegedPolicyName} \
#                                        --region ${AWS::Region} \
#                                        --stage ${RandomStringResource.RandomString}"
