#!/bin/sh
rsync -avr --progress --stats --exclude-from='rsync_ignore_out.txt' ./ availab-dl3:~/Sandboxes/rocket_landing_sac/ --delete
rsync -avr --progress --stats --exclude-from='rsync_ignore_out.txt' ./ availab-dl4:~/Sandboxes/rocket_landing_sac/ --delete
