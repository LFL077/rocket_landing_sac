_RUNS_PER_GPU = 3

# read the lines and grab the url
sweep_id = ""
project_id = ""
with open("./sweep_setup/temp.out", "r") as f:
    # read lines
    lines = f.readlines()

    # find the url
    for line in lines:
        if "Run sweep agent with:" in line:
            sweep_id = line.split("/")[-1]
            project_id = line.split("/")[-2]
            sweep_id = sweep_id.replace("\n", "")

top_lines = """#!/bin/bash

# this file has been automatically generated, do not edit manually

source venv/bin/activate
declare -a pids=()
"""

run_line = f"wandb agent jjshoots/{project_id}/{sweep_id} --count 1 & "

joining_lines = """
pids+=($!)
sleep 10
"""

end_lines = """
for pid in ${pids[*]}; do
    wait $pid
done
"""

# write for availab machines
with open("./sweep_setup/run_sweep.sh", "w") as f:
    # shebangs
    f.write(top_lines)

    # contents
    for _ in range(_RUNS_PER_GPU):
        f.write(run_line)
        f.write(joining_lines)

    # closing
    f.write(end_lines)
