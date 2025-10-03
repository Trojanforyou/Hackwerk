#!/bin/bash
# Dutch Government Portal - Quick Start Script

# Get the directory of the script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Default port
PORT=${1:-8501}

echo "🚀 Starting Dutch Government Portal..."
echo "📁 Working directory: $DIR"
echo "🌐 Port: $PORT"
echo "🔗 URL: http://localhost:$PORT"
echo ""

# Kill any existing streamlit processes
pkill -f streamlit 2>/dev/null
sleep 1

# Start the application
"$DIR/venv_new/bin/python" -m streamlit run "$DIR/app.py" --server.port "$PORT"