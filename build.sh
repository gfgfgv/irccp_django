#!/usr/bin/env bash
# Render (and similar platforms) run this once on every deploy, before
# starting the app with the Start Command. See README "Деплой" for setup.
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py seed_news
python manage.py seed_logos
