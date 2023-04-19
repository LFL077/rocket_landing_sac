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

# sync code out
rsync -avr --progress --stats --exclude-from='rsync_ignore_out.txt' ./ availab-dl3:~/Sandboxes/rocket_landing_sac/ --delete
rsync -avr --progress --stats --exclude-from='rsync_ignore_out.txt' ./ availab-dl4:~/Sandboxes/rocket_landing_sac/ --delete

# run code on server
ssh availab-dl3 'tmux send-keys -t 0 "./sweep_setup/run_sweep.sh" ENTER' &
ssh availab-dl4 'tmux send-keys -t 0 "./sweep_setup/run_sweep.sh" ENTER' &

echo "Please run ./sweep_setup/run_sweep.sh."
