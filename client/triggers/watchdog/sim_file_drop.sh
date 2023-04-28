#!/bin/bash

# signal file
signal_file=NISAR_S198_WFF_WG5_M00_P00523_R00_C00_G01_2023_057_03_04_50_141200000.ldf

# stage raw data
for i in $(cat ${signal_file} | jq --raw-output '.files[].name'); do
  touch tmp/${i}
done

# stage signal file
cp ${signal_file} tmp/