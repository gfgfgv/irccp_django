"""Runs core.management.commands.fetch_news on a recurring schedule, in a
background thread inside the same Django process. Started from
core/apps.py::CoreConfig.ready().

This is deliberately simple (APScheduler, in-process) rather than
Celery+Redis, since the goal is "news update themselves every few hours"
for a single `runserver` / single-process deployment. If you later move to
a multi-worker production setup (gunicorn with several workers, several
server instances, etc.), switch this to a proper task queue (Celery beat,
django-crontab, or an OS-level cron job calling
`python manage.py fetch_news`) so the job doesn't run once per worker.
"""

import logging
import threading

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.conf import settings

logger = logging.getLogger(__name__)

_scheduler = None


def _run_fetch_job():
    from django.core.management import call_command

    try:
        call_command("fetch_news")
    except Exception:
        logger.exception("Scheduled RSS fetch_news job failed")


def start_scheduler():
    global _scheduler
    if _scheduler is not None:
        return  # already running

    interval_hours = getattr(settings, "RSS_FETCH_INTERVAL_HOURS", 6)

    _scheduler = BackgroundScheduler(daemon=True)
    _scheduler.add_job(
        _run_fetch_job,
        trigger=IntervalTrigger(hours=interval_hours),
        id="fetch_news_job",
        max_instances=1,
        replace_existing=True,
    )
    _scheduler.start()
    logger.info("RSS auto-fetch scheduler started: every %s hour(s)", interval_hours)

    # Also run once shortly after startup, so news shows up without waiting
    # a full interval the first time the server is started.
    threading.Timer(10, _run_fetch_job).start()
