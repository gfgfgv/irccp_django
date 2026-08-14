from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from core.models import Category, CategoryLogo, SiteBranding

DEFAULT_LOGOS_DIR = Path(__file__).resolve().parent.parent.parent / "default_logos"

CATEGORY_FILES = {
    Category.FIRE_SAFETY: "fire_safety.jpeg",
    Category.CBRN: "cbrn.jpeg",
    Category.EOD: "eod.jpeg",
    Category.DISASTER_MEDICINE: "disaster_medicine.jpeg",
    Category.ENVIRONMENTAL_SAFETY: "environmental_safety.jpeg",
}
SITE_LOGO_FILE = "site_logo.jpeg"


class Command(BaseCommand):
    help = (
        "Load the bundled default logo images (core/default_logos/) into the "
        "database as the initial CategoryLogo/SiteBranding rows. Safe to "
        "re-run: it only fills in what's missing and never overwrites a logo "
        "you've already changed via /admin/. Use --force to overwrite anyway."
    )

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true",
                             help="Replace existing logos with the bundled defaults.")

    def handle(self, *args, **options):
        force = options["force"]

        for category, filename in CATEGORY_FILES.items():
            path = DEFAULT_LOGOS_DIR / filename
            if not path.exists():
                self.stderr.write(self.style.WARNING(f"Missing bundled file: {path}"))
                continue

            existing = CategoryLogo.objects.filter(category=category).first()
            if existing and not force:
                self.stdout.write(f"Skipped {category} (logo already set)")
                continue

            obj = existing or CategoryLogo(category=category)
            with open(path, "rb") as fh:
                obj.image.save(filename, File(fh), save=True)
            self.stdout.write(self.style.SUCCESS(f"Set logo for {category}"))

        site_path = DEFAULT_LOGOS_DIR / SITE_LOGO_FILE
        if site_path.exists():
            existing = SiteBranding.objects.first()
            if existing and not force:
                self.stdout.write("Skipped site logo (already set)")
            else:
                obj = existing or SiteBranding()
                with open(site_path, "rb") as fh:
                    obj.image.save(SITE_LOGO_FILE, File(fh), save=True)
                self.stdout.write(self.style.SUCCESS("Set main site logo"))
        else:
            self.stderr.write(self.style.WARNING(f"Missing bundled file: {site_path}"))

        self.stdout.write(self.style.SUCCESS("Done."))
