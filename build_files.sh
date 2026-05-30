#!/bin/bash
set -e
echo "BUILD START"

# Ensure the directory exists
mkdir -p staticfiles_build/static

echo "Installing requirements..."
python3 -m pip install -r requirements.txt

echo "Collecting static files (using test_settings to bypass DB connection requirements)..."
python3 manage.py collectstatic --noinput --clear --settings=helpinghand.test_settings

echo "BUILD END"
