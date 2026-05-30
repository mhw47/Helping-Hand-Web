#!/bin/bash

echo "=== VERCEL BUILD INITIATED ==="

# Force build directory creation
mkdir -p staticfiles_build/static

echo "Upgrading base installer utilities..."
python3 -m pip install --upgrade pip setuptools wheel --no-cache-dir

echo "Installing project requirements..."
# Try installing normally with pre-compiled packages prioritized
if ! python3 -m pip install -r requirements.txt --prefer-binary --no-cache-dir; then
    echo "ERROR: Pip installation broke. Attempting fallback installation..."
    # Fallback to help point out which package is breaking
    python3 -m pip install Django python-dotenv django-extensions whitenoise --no-cache-dir
fi

echo "Running Django collectstatic..."
python3 manage.py collectstatic --noinput --clear

echo "=== VERCEL BUILD COMPLETE ==="
