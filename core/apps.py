import os

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        # Django's `runserver` autoreloader launches a watcher process plus a
        # worker process; only the worker process sets RUN_MAIN=true. Without
        # this guard the scheduler would start twice and fetch everything twice.
        if os.environ.get("RUN_MAIN") != "true":
            return

        from django.conf import settings

        if not getattr(settings, "RSS_AUTO_FETCH", True):
            return

        from core.scheduler import start_scheduler

        start_scheduler()
