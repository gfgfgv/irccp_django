from django.core.management.base import BaseCommand

from core import data
from core.models import Journal, Resource


class Command(BaseCommand):
    help = (
        "One-time import: loads the old core/data.py RESOURCES/JOURNALS lists "
        "into the Resource/Journal database tables, so they become editable "
        "from /admin/. Safe to re-run — matches by name/title and only fills "
        "in what's missing, never overwrites anything you've since changed "
        "in the admin."
    )

    def handle(self, *args, **options):
        created_resources = 0
        for i, r in enumerate(data.RESOURCES):
            _, was_created = Resource.objects.get_or_create(
                name=r["name"],
                defaults=dict(
                    url=r["url"],
                    desc=r["desc"],
                    category=r["cat"],
                    logo_url=r.get("logo_url", ""),
                    fallback_image_url=(
                        f"https://images.unsplash.com/{r['img']}?w=400&h=200&fit=crop&auto=format"
                        if r.get("img") else ""
                    ),
                    order=i,
                ),
            )
            created_resources += int(was_created)

        created_journals = 0
        for i, j in enumerate(data.JOURNALS):
            _, was_created = Journal.objects.get_or_create(
                title=j["title"],
                defaults=dict(
                    publisher=j["pub"],
                    url=j["url"],
                    category=j["cat"],
                    impact_factor=j.get("if_", "—"),
                    desc=j["desc"],
                    logo_url=j.get("logo_url", ""),
                    order=i,
                ),
            )
            created_journals += int(was_created)

        self.stdout.write(self.style.SUCCESS(
            f"Resources: {created_resources} created, "
            f"{len(data.RESOURCES) - created_resources} already existed."
        ))
        self.stdout.write(self.style.SUCCESS(
            f"Journals: {created_journals} created, "
            f"{len(data.JOURNALS) - created_journals} already existed."
        ))
