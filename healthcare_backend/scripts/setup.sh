#!/usr/bin/env bash
set -euo pipefail
python manage.py makemigrations accounts patients doctors mappings
python manage.py migrate
python manage.py check
