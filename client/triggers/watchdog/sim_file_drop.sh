#!/bin/bash
COUNT=$1
for i in $(seq 1 $COUNT); do
  touch tmp/NISAR_asdf${i}.h5
done
