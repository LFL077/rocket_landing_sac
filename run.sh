#!/bin/bash

######################################################################################################
# setup the sweep
######################################################################################################
echo "Generating sweep..."
wandb sweep sweep_setup/sweep.yaml &> ./sweep_setup/temp.out

# automatically generate sh file for availab servers
echo "Generating run.sh"
python3 sweep_setup/make_sweep_runs.py

# remove the temp file
rm ./sweep_setup/temp.out

# make executable
chmod +x ./sweep_setup/run_sweep.sh

echo "Please run ./sweep_setup/run_sweep.sh."
