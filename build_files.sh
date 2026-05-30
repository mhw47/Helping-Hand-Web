#!/bin/bash
set -e
echo "BUILD START"

# Ensure the directory exists so Vercel doesn't fail the build immediately if the script crashes
mkdir -p staticfiles_build/static

# Use generic python3 to avoid version-specific missing binary errors
python3 -m pip install -r requirements.txt
python3 manage.py collectstatic --noinput --clear

echo "BUILD END"
