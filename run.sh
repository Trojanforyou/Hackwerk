#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

PORT=${1:-8501}

pkill -f streamlit 2>/dev/null
sleep 1

"$DIR/venv_new/bin/python" -m streamlit run "$DIR/app.py" --server.port "$PORT"

#to run it u just need to type "./run.sh" and some port for example 8555 or something else