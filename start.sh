#!/bin/bash
echo "========================================="
echo "      OAAI Model-Radar - by OAAI.xyz     "
echo "========================================="
echo ""
echo "Starting server on http://127.0.0.1:5000"
echo ""

# Try to open the browser automatically in background
(
    sleep 2
    if command -v xdg-open &> /dev/null; then
        xdg-open http://127.0.0.1:5000
    elif command -v open &> /dev/null; then
        open http://127.0.0.1:5000
    else
        echo "Please open http://127.0.0.1:5000 manually in your browser."
    fi
) &

# Run the python server directly
python3 server.py || python server.py
