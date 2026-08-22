"""RSS feed sources for the news auto-import job.

Each entry maps one real, publicly available RSS feed to the IRCCP category
its items should be filed under. Add or remove feeds here — the fetch job
picks this list up automatically, no other code changes needed.

Verified working as of Aug 2026. If a feed URL ever changes or goes offline,
`fetch_news` will just log a warning for that feed and continue with the
others — it won't crash the whole job.
"""

from .models import Category

RSS_FEEDS = [
    {
        "name": "ReliefWeb Updates",
        "url": "https://reliefweb.int/updates/rss.xml",
        "category": Category.DISASTER_MEDICINE,
    },
    {
        "name": "IAEA Top News",
        "url": "https://www.iaea.org/feeds/topnews",
        "category": Category.CBRN,
    },
    {
        "name": "UNEP News & Stories",
        "url": "https://www.unep.org/news-and-stories/rss.xml",
        "category": Category.ENVIRONMENTAL_SAFETY,
    },
    {
        "name": "FEMA Disaster Declarations",
        "url": "https://www.fema.gov/news/disasters_rss.fema",
        "category": Category.FIRE_SAFETY,
    },
    # No reliable public RSS feed was found for EOD-specific news at the time
    # this was written (GICHD and similar mine-action bodies don't publish
    # one). Add one here if you find a suitable source, e.g.:
    # {
    #     "name": "Your EOD source",
    #     "url": "https://example.org/rss.xml",
    #     "category": Category.EOD,
    # },
]

# Simple keyword override: if an entry's title/summary contains any of these
# words, file it under that category instead of the feed's default. This
# lets one broad feed (like ReliefWeb) still populate more specific
# categories when relevant.
CATEGORY_KEYWORDS = {
    Category.EOD: ["explosive ordnance", "landmine", "demining", "mine action", "unexploded", "ied "],
    Category.CBRN: ["chemical weapon", "radiological", "biological weapon", "nuclear safety", "cbrn"],
    Category.FIRE_SAFETY: ["wildfire", "fire safety", "fire brigade", " fire ", "firefighter"],
}


# ---------------------------------------------------------------------------
# Events auto-import (core/management/commands/fetch_events.py)
# ---------------------------------------------------------------------------
# Same idea as RSS_FEEDS above, but for the Events page. Each entry is one
# real, publicly reachable feed of upcoming events.
#
# "type" can be:
#   "rss"   — a normal RSS/Atom feed (parsed with feedparser, same as news).
#             Most RSS feeds don't carry a structured event date/location,
#             so fetch_events tries to pull a date out of the entry text; if
#             it can't find one, that entry is skipped rather than guessed.
#   "ical"  — an iCalendar (.ics) feed (parsed with the `icalendar` package).
#             This is the more reliable option for events, since iCal
#             entries have real DTSTART/LOCATION/SUMMARY fields — many event
#             platforms (Localist, Plone-based sites, Google/Outlook
#             calendar exports, etc.) publish one even when they don't
#             publish RSS.
#
# As of Aug 2026, none of the ~20 Fire Safety / CBRN / EOD / Disaster
# Medicine / Environmental Safety event sites checked (thebigredguide,
# clocate, 10times, cbrneworld, ctif.org, sfpe.org, eodcoe.org, wadem.org,
# unece.org, genevaenvironmentnetwork.org, etc.) had a confirmed, freely
# accessible RSS or iCal feed for their event listings — aggregators like
# 10times/clocate only expose event data through paid scraping APIs, and
# the standalone organisation sites are plain HTML with no feed. So this
# list ships empty. Add events for now through /admin/ → Core → Events.
#
# To wire up a real feed once you find one, just add an entry here, e.g.:
# EVENT_FEEDS = [
#     {
#         "name": "CTIF Events",
#         "url": "https://ctif.org/events/rss.xml",
#         "type": "rss",
#         "category": Category.FIRE_SAFETY,
#     },
#     {
#         "name": "UNECE Meetings",
#         "url": "https://unece.org/events/ical",
#         "type": "ical",
#         "category": Category.ENVIRONMENTAL_SAFETY,
#     },
# ]
EVENT_FEEDS = []
