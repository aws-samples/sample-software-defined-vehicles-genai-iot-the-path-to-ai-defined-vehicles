#!/bin/sh
echo "===== ACTIVATING VIRTUAL ENVIRONMENT ====="
echo "working directory: $(pwd)"
echo "requirements path $1"
python3 -m venv venv
pip install --upgrade pip
source venv/bin/activate
echo "===== INSTALLING DEPENDENCIES ====="

python3 -m pip install -r $1

echo "===== DONE ====="

