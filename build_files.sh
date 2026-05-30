#!/bin/bash
echo "BUILD START"

# Create fallback directory
mkdir -p staticfiles_build/static

echo "Installing requirements..."
# Added --no-cache-dir and --disable-pip-version-check flags to bypass environment freezes
python3 -m pip install --no-cache-dir --disable-pip-version-check -r requirements.txt || { echo 'Pip install failed'; exit 1; }

echo "Running Django collectstatic..."
python3 manage.py collectstatic --noinput --clear || { echo 'Collectstatic failed'; exit 1; }

echo "BUILD END"
