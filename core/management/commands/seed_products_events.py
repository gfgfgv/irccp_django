from django.core.management.base import BaseCommand

from core import data
from core.models import Company, Event


class Command(BaseCommand):
    help = (
        "One-time import: loads the starter PRODUCTS/EVENTS lists from "
        "core/data.py into the Company/Event database tables, so the "
        "Products and Events pages aren't empty on a fresh install. Safe to "
        "re-run — matches by name/title and only fills in what's missing, "
        "never overwrites anything you've since changed in the admin."
    )

    def handle(self, *args, **options):
        created_companies = 0
        for i, c in enumerate(data.PRODUCTS):
            _, was_created = Company.objects.get_or_create(
                name=c["name"],
                defaults=dict(
                    url=c["url"],
                    desc=c["desc"],
                    category=c["cat"],
                    logo_url=c.get("logo_url", ""),
                    order=i,
                ),
            )
            created_companies += int(was_created)

        created_events = 0
        for i, e in enumerate(data.EVENTS):
            _, was_created = Event.objects.get_or_create(
                title=e["title"],
                defaults=dict(
                    date=e["date"],
                    end_date=e.get("end_date") or None,
                    location=e.get("location", ""),
                    category=e["cat"],
                    desc=e["desc"],
                    registration_url=e.get("registration_url", ""),
                    order=i,
                ),
            )
            created_events += int(was_created)

        self.stdout.write(self.style.SUCCESS(
            f"Companies: {created_companies} created, "
            f"{len(data.PRODUCTS) - created_companies} already existed."
        ))
        self.stdout.write(self.style.SUCCESS(
            f"Events: {created_events} created, "
            f"{len(data.EVENTS) - created_events} already existed."
        ))
