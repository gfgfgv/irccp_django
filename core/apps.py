import os
import sys

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        from django.conf import settings

        if not getattr(settings, "RSS_AUTO_FETCH", True):
            return

        if "runserver" in sys.argv:
            # Django's `runserver` autoreloader launches a watcher process
            # plus a worker process; only the worker process sets
            # RUN_MAIN=true. Skip the watcher so the scheduler doesn't start
            # twice locally.
            if os.environ.get("RUN_MAIN") != "true":
                return
        elif sys.argv and sys.argv[0].endswith("manage.py"):
            # Any other one-off manage.py command (migrate, seed_news,
            # createsuperuser, collectstatic, etc. — e.g. everything
            # build.sh runs) — these aren't a running server, so don't spin
            # up a background scheduler for them.
            return
        # Anything else (gunicorn, uwsgi, daphne, ...) means we're actually
        # serving the app — including on Render, where RUN_MAIN is never
        # set at all. Start the scheduler in that case.

        from core.scheduler import start_scheduler

        start_scheduler()
