#!/bin/bash

cleanup() {
    echo "Stopping all background processes..."
    kill -TERM -$$ 2>/dev/null
    sleep 2
    kill -KILL -$$ 2>/dev/null
    echo "All processes stopped"
    exit 0
}

trap cleanup SIGINT SIGTERM

source ./source_config.sh
python worker.py &

python client.py 