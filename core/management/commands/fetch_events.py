"""Fetch upcoming events from the feeds configured in core/rss_config.py
(EVENT_FEEDS) and import new ones into the Event model.

Mirrors fetch_news.py's structure and safety behaviour: a broken/unreachable
feed is logged and skipped, it never crashes the whole run, and items already
imported (matched by source_url) are never re-created.

Supports two feed types:
  - "rss":  parsed with feedparser. Since plain RSS items rarely carry a
            structured event date, we try to find one in the entry's title
            or summary text; if no date can be found, the entry is skipped
            (we never guess/fabricate an event date).
  - "ical": parsed with the `icalendar` package. iCalendar VEVENTs have a
            real DTSTART/DTEND/LOCATION/SUMMARY, so these are the more
            reliable source when available.
"""

import html
import logging
import re
import urllib.request
from datetime import date, datetime

import feedparser
from dateutil import parser as dateutil_parser
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from icalendar import Calendar

from core.models import Event
from core.rss_config import CATEGORY_KEYWORDS, EVENT_FEEDS

logger = logging.getLogger(__name__)

MAX_ITEMS_PER_FEED = 15
TAG_RE = re.compile(r"<[^>]+>")
REQUEST_TIMEOUT = 15


def clean_text(raw_html: str, limit: int = 500) -> str:
    text = TAG_RE.sub(" ", raw_html or "")
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > limit:
        text = text[:limit].rsplit(" ", 1)[0] + "…"
    return text


def guess_category(title: str, summary: str, default_category: str) -> str:
    haystack = f"{title} {summary}".lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in haystack for keyword in keywords):
            return category
    return default_category


def as_date(value) -> date:
    """Coerce an icalendar dt value (date or datetime) into a plain date."""
    if isinstance(value, datetime):
        return value.date()
    return value


MONTH_NAMES = (
    r"Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|"
    r"Aug(?:ust)?|Sep(?:t|tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?"
)

# Each tuple is (compiled pattern, cleanup function) — cleanup turns whatever
# the pattern matched (which may include a day range, e.g. "3 - 5 November
# 2026") into a single parseable "start date" string.
DATE_PATTERN_SPECS = [
    (
        # "15 October 2026" or "3 - 5 November 2026" (day[-day] Month Year)
        re.compile(rf"\b(\d{{1,2}})(?:st|nd|rd|th)?(?:\s*[-–]\s*\d{{1,2}}(?:st|nd|rd|th)?)?\s+({MONTH_NAMES})\.?\s+(\d{{4}})\b", re.I),
        lambda m: f"{m.group(1)} {m.group(2)} {m.group(3)}",
    ),
    (
        # "October 15, 2026" or "October 15-17, 2026" (Month day[-day], Year)
        re.compile(rf"\b({MONTH_NAMES})\.?\s+(\d{{1,2}})(?:st|nd|rd|th)?(?:\s*[-–]\s*\d{{1,2}}(?:st|nd|rd|th)?)?,?\s+(\d{{4}})\b", re.I),
        lambda m: f"{m.group(1)} {m.group(2)} {m.group(3)}",
    ),
    (
        # ISO "2026-10-15"
        re.compile(r"\b(\d{4}-\d{2}-\d{2})\b"),
        lambda m: m.group(1),
    ),
]


def find_date_in_text(*texts) -> date | None:
    """Best-effort: look for a real calendar date somewhere in the given
    strings, using pattern matching first (dateutil's fuzzy mode is too
    unreliable on full paragraphs). Returns None (never guesses) if nothing
    confident is found."""
    haystack = " ".join(t for t in texts if t)
    for pattern, cleanup in DATE_PATTERN_SPECS:
        match = pattern.search(haystack)
        if not match:
            continue
        candidate = cleanup(match)
        try:
            return dateutil_parser.parse(candidate).date()
        except (ValueError, OverflowError):
            continue
    return None


class Command(BaseCommand):
    help = "Fetch upcoming events from the configured feeds (core/rss_config.py: EVENT_FEEDS) and import new ones."

    def handle(self, *args, **options):
        if not EVENT_FEEDS:
            self.stdout.write(self.style.WARNING(
                "EVENT_FEEDS is empty in core/rss_config.py — nothing to fetch. "
                "Add events manually via /admin/ (Core → Events), or add a real "
                "RSS/iCal feed URL to EVENT_FEEDS once you find one."
            ))
            return

        total_created = 0
        total_seen = 0

        for feed in EVENT_FEEDS:
            feed_type = feed.get("type", "rss")
            self.stdout.write(f"Fetching: {feed['name']} ({feed['url']}, {feed_type})")
            try:
                if feed_type == "ical":
                    created = self._handle_ical(feed)
                else:
                    created = self._handle_rss(feed)
            except Exception as exc:  # network errors, malformed feeds, etc.
                logger.warning("Failed to fetch event feed %s: %s", feed["url"], exc)
                self.stderr.write(self.style.WARNING(f"  skipped (fetch error): {exc}"))
                continue

            total_created += created
            self.stdout.write(f"  +{created} new event(s)")

        self.stdout.write(self.style.SUCCESS(
            f"Done. Imported {total_created} new event(s) across {len(EVENT_FEEDS)} feed(s)."
        ))

    def _handle_rss(self, feed) -> int:
        parsed = feedparser.parse(feed["url"])
        if parsed.bozo and not parsed.entries:
            self.stderr.write(self.style.WARNING(f"  skipped (unparseable feed): {parsed.bozo_exception}"))
            return 0

        created = 0
        for entry in parsed.entries[:MAX_ITEMS_PER_FEED]:
            link = getattr(entry, "link", "")
            title = getattr(entry, "title", "").strip()
            if not title or not link:
                continue
            if Event.objects.filter(source_url=link).exists():
                continue

            raw_summary = getattr(entry, "summary", "") or getattr(entry, "description", "")
            summary = clean_text(raw_summary)

            event_date = find_date_in_text(title, summary)
            if event_date is None:
                # No confident date found in the text — skip rather than guess.
                continue

            category = guess_category(title, summary, feed["category"])
            Event.objects.create(
                title=title[:255],
                date=event_date,
                location="",
                category=category,
                desc=summary or title,
                registration_url=link,
                source_url=link,
                is_auto_imported=True,
            )
            created += 1
        return created

    def _handle_ical(self, feed) -> int:
        req = urllib.request.Request(feed["url"], headers={"User-Agent": "IRCCP-EventBot/1.0"})
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as response:
            raw = response.read()

        cal = Calendar.from_ical(raw)
        created = 0
        count = 0
        for component in cal.walk():
            if component.name != "VEVENT" or count >= MAX_ITEMS_PER_FEED:
                continue
            count += 1

            title = str(component.get("summary", "")).strip()
            dtstart = component.get("dtstart")
            if not title or not dtstart:
                continue
            event_date = as_date(dtstart.dt)

            dtend = component.get("dtend")
            end_date = as_date(dtend.dt) if dtend else None
            if end_date == event_date:
                end_date = None

            url_prop = component.get("url")
            source_key = str(url_prop) if url_prop else f"{feed['url']}#{component.get('uid', title)}"
            if Event.objects.filter(source_url=source_key).exists():
                continue

            location = str(component.get("location", ""))
            desc = clean_text(str(component.get("description", "")))
            category = guess_category(title, desc, feed["category"])

            Event.objects.create(
                title=title[:255],
                date=event_date,
                end_date=end_date,
                location=location[:255],
                category=category,
                desc=desc or title,
                registration_url=str(url_prop) if url_prop else "",
                source_url=source_key,
                is_auto_imported=True,
            )
            created += 1
        return created
