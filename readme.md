# Sup, homie.

## Installation

`pip3 install -e . -r requirements.txt`

This depends on the env `PyFlyt/Rocket-Landing-v0`, so if you want to modify behaviours install a local, editable version of PyFlyt and use that.

## Usage

### Training

`python3 src/main.py --train`

### Demonstrating

`python3 src/main.py --display --version=XXXXX`

Replace `XXXXX` with the version number assigned in the training script.

To render and save a gif, do:

`python3 src/main.py --display --version=XXXXX --render_gif`
