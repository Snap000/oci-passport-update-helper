#!/bin/bash
# OCI Photo Prep - double-click me (Mac). First time: right-click > Open.
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null; then
  echo "Python 3 is not installed. Opening python.org - install it, then double-click this again."
  open https://www.python.org/downloads/; read -p "Press Enter to close"; exit 1
fi
echo "Installing helper tools (first run only)..."
python3 -m pip install --user -q -r requirements.txt
python3 scripts/oci_prep.py auto MyFiles
open MyFiles
read -p "Done. Press Enter to close"
