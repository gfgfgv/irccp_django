"""Runs core.management.commands.fetch_news and fetch_events on recurring
schedules, in a background thread inside the same Django process. Started
from core/apps.py::CoreConfig.ready().

This is deliberately simple (APScheduler, in-process) rather than
Celery+Redis, since the goal is "content updates itself every so often" for
a single `runserver` / single-process deployment. If you later move to a
multi-worker production setup (gunicorn with several workers, several
server instances, etc.), switch this to a proper task queue (Celery beat,
django-crontab, or an OS-level cron job calling
`python manage.py fetch_news` / `fetch_events`) so the jobs don't run once
per worker.
"""

import logging
import threading

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.conf import settings

logger = logging.getLogger(__name__)

_scheduler = None


def _run_news_job():
    from django.core.management import call_command

    try:
        call_command("fetch_news")
    except Exception:
        logger.exception("Scheduled RSS fetch_news job failed")


def _run_events_job():
    from django.core.management import call_command

    try:
        call_command("fetch_events")
    except Exception:
        logger.exception("Scheduled fetch_events job failed")


def start_scheduler():
    global _scheduler
    if _scheduler is not None:
        return  # already running

    news_interval_hours = getattr(settings, "RSS_FETCH_INTERVAL_HOURS", 6)
    events_interval_hours = getattr(settings, "EVENT_FETCH_INTERVAL_HOURS", 24)

    _scheduler = BackgroundScheduler(daemon=True)
    _scheduler.add_job(
        _run_news_job,
        trigger=IntervalTrigger(hours=news_interval_hours),
        id="fetch_news_job",
        max_instances=1,
        replace_existing=True,
    )
    _scheduler.add_job(
        _run_events_job,
        trigger=IntervalTrigger(hours=events_interval_hours),
        id="fetch_events_job",
        max_instances=1,
        replace_existing=True,
    )
    _scheduler.start()
    logger.info("News auto-fetch scheduler started: every %s hour(s)", news_interval_hours)
    logger.info("Events auto-fetch scheduler started: every %s hour(s)", events_interval_hours)

    # Also run both once shortly after startup, so content shows up without
    # waiting a full interval the first time the server is started. Staggered
    # a few seconds apart so they don't both hit the network at once.
    threading.Timer(10, _run_news_job).start()
    threading.Timer(20, _run_events_job).start()
