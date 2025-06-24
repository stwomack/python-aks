#!/bin/bash
# Start the worker in the background
source ./source_config.sh
python worker.py &
# Start the client
python client.py