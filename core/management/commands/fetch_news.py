import html
import logging
import re
from datetime import date, datetime

import feedparser
from django.core.management.base import BaseCommand
from django.utils.timezone import now

from core.models import NewsItem
from core.rss_config import CATEGORY_KEYWORDS, RSS_FEEDS

logger = logging.getLogger(__name__)

MAX_ITEMS_PER_FEED = 8
TAG_RE = re.compile(r"<[^>]+>")


def clean_summary(raw_html: str, limit: int = 500) -> str:
    """Strip HTML tags/entities from an RSS summary and trim it to `limit` chars."""
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


def entry_date(entry) -> date:
    for field in ("published_parsed", "updated_parsed"):
        value = getattr(entry, field, None)
        if value:
            return datetime(*value[:6]).date()
    return now().date()


def entry_image(entry) -> str:
    media = getattr(entry, "media_content", None) or getattr(entry, "media_thumbnail", None)
    if media and isinstance(media, list) and media[0].get("url"):
        return media[0]["url"]
    for link in getattr(entry, "links", []):
        if link.get("type", "").startswith("image/"):
            return link.get("href", "")
    return ""


class Command(BaseCommand):
    help = "Fetch news items from the configured RSS feeds (core/rss_config.py) and import new ones."

    def handle(self, *args, **options):
        total_created = 0
        total_seen = 0

        for feed in RSS_FEEDS:
            self.stdout.write(f"Fetching: {feed['name']} ({feed['url']})")
            try:
                parsed = feedparser.parse(feed["url"])
            except Exception as exc:  # network errors, malformed feeds, etc.
                logger.warning("Failed to fetch feed %s: %s", feed["url"], exc)
                self.stderr.write(self.style.WARNING(f"  skipped (fetch error): {exc}"))
                continue

            if parsed.bozo and not parsed.entries:
                self.stderr.write(self.style.WARNING(f"  skipped (unparseable feed): {parsed.bozo_exception}"))
                continue

            created_for_feed = 0
            for entry in parsed.entries[:MAX_ITEMS_PER_FEED]:
                total_seen += 1
                link = getattr(entry, "link", "")
                title = getattr(entry, "title", "").strip()
                if not title or not link:
                    continue

                if NewsItem.objects.filter(source_url=link).exists():
                    continue

                raw_summary = getattr(entry, "summary", "") or getattr(entry, "description", "")
                summary = clean_summary(raw_summary)
                category = guess_category(title, summary, feed["category"])

                NewsItem.objects.create(
                    title=title[:500],
                    summary=summary or title,
                    category=category,
                    source=feed["name"],
                    date=entry_date(entry),
                    image_url=entry_image(entry),
                    source_url=link,
                    is_auto_imported=True,
                )
                created_for_feed += 1
                total_created += 1

            self.stdout.write(f"  +{created_for_feed} new item(s)")

        self.stdout.write(self.style.SUCCESS(
            f"Done. Checked {total_seen} entries across {len(RSS_FEEDS)} feed(s), imported {total_created} new."
        ))
