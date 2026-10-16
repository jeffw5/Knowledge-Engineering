#!/bin/bash
# Double-click in Finder to start the KE Workbench.
# Stops any older proxy on port 3000, starts this folder's proxy.py and opens the browser.
cd "$(dirname "$0")"
PORT="${PORT:-3000}"
OLD=$(lsof -ti tcp:$PORT 2>/dev/null)
if [ -n "$OLD" ]; then echo "Stopping the old server on port $PORT ($OLD)"; kill $OLD; sleep 1; fi
OPEN=1 python3 proxy.py
echo
echo "The workbench server has stopped. Press Return to close this window."
read
