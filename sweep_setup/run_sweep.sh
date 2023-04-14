#!/bin/bash

# this file has been automatically generated, do not edit manually

source venv/bin/activate
declare -a pids=()
wandb agent jjshoots/CCGE2_oracle_search/7dsq2cw1 --count 1 & 
pids+=($!)
sleep 10
wandb agent jjshoots/CCGE2_oracle_search/7dsq2cw1 --count 1 & 
pids+=($!)
sleep 10
wandb agent jjshoots/CCGE2_oracle_search/7dsq2cw1 --count 1 & 
pids+=($!)
sleep 10

for pid in ${pids[*]}; do
    wait $pid
done
