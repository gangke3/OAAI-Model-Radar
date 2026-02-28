#!/bin/bash
cd "$(dirname "$0")" || exit
echo "========================================="
echo "      OAAI Model-Radar - by OAAI.xyz     "
echo "========================================="
echo ""
echo "Starting server on http://127.0.0.1:5000"
echo ""



# Run the python server directly
python3 server.py || python server.py
