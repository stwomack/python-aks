#!/bin/bash
# Start the worker in the background
python worker.py &
# Start the client
python client.py