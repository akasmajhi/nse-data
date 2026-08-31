#!/bin/bash

START_TIME=$SECONDS
# Place the commands you want to time here
# sleep 5
python src/core.py
END_TIME=$SECONDS

DURATION=$((END_TIME - START_TIME))
echo "Script finished in $DURATION seconds."

# Alternatively, set SECONDS to 0 before the timed event
# SECONDS=0
# Place commands here
# sleep 2
# echo "Timed section finished in $SECONDS seconds."
