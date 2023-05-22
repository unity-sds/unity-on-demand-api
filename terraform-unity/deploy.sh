#!/bin/bash
set -ex

# install conda
curl -sSL https://repo.anaconda.com/miniconda/Miniconda3-py39_22.11.1-1-Linux-x86_64.sh -o /tmp/install_miniconda.sh
chmod 755 /tmp/install_miniconda.sh
bash /tmp/install_miniconda.sh -b -p /usr/local -u

# install serverless
npm install -g serverless

# print serverless version
serverless --version

# clone unity-on-demand-api repo
git clone https://github.com/unity-sds/unity-on-demand-api.git
cd unity-on-demand-api

# export serverless args
export sls_args="--param cluster_name=unity-sps-on-demand-${RandomString} \
  --param sps_api_url=http://${sps_api}:5002 \
  --param permissionsBoundaryPolicyName=${PrivilegedPolicyName} \
  --region ${region} \
  --stage ${RandomString}"

# deploy
serverless plugin install -n serverless-python-requirements
serverless plugin install -n serverless-wsgi
serverless deploy $sls_args

# output deployment info
serverless info --verbose $sls_args > /tmp/deployment_info.yaml
