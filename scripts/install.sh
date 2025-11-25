#!/usr/bin/env bash
set -euo pipefail

# Create a virtualenv and install dependencies
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
	python3 -m venv "$VENV_DIR"
fi
"$VENV_DIR/bin/python" -m pip install --upgrade pip
"$VENV_DIR/bin/python" -m pip install -r requirements.txt

echo "Install complete. Activate the venv with: source $VENV_DIR/bin/activate"
echo "Verify by running: $VENV_DIR/bin/python scripts/check_ray.py"
