from datetime import date

from django.core.management.base import BaseCommand

from core.models import Category, NewsItem

NEWS = [
    dict(title="WHO Releases Updated Mass Casualty Incident Management Framework",
         summary="The World Health Organization published revised guidelines incorporating lessons from recent natural disasters in Southeast Asia and the Middle East, strengthening international coordination mechanisms for medical response teams.",
         category=Category.DISASTER_MEDICINE, source="World Health Organization",
         date=date(2026, 6, 28), image_url="https://images.unsplash.com/photo-1551601651-2a8555f1a136?w=400&h=200&fit=crop&auto=format"),
    dict(title="EU CBRN Action Plan 2026–2030 Formally Adopted by European Commission",
         summary="The Commission adopted a new CBRN Action Plan expanding detection capabilities and cross-border response coordination across all 27 member states, backed by €480 million in dedicated funding.",
         category=Category.CBRN, source="European Commission",
         date=date(2026, 6, 19), image_url="https://images.unsplash.com/photo-1582719508461-905c673771fd?w=400&h=200&fit=crop&auto=format"),
    dict(title="UNDRR: Urban Wildfire Risk Has Tripled Over Past Decade",
         summary="A landmark UNDRR report identifies urban-wildland interface zones as the fastest-growing fire risk category globally, urging immediate policy revision and improved firefighter training standards.",
         category=Category.FIRE_SAFETY, source="UN Office for Disaster Risk Reduction",
         date=date(2026, 6, 12), image_url="https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=400&h=200&fit=crop&auto=format"),
    dict(title="NATO Operation IRON SWEEP 2026 Validates Robotic EOD Protocols",
         summary="EOD teams from 14 NATO nations completed Operation IRON SWEEP in Poland, successfully testing next-generation remote disposal systems under simulated urban conflict conditions.",
         category=Category.EOD, source="NATO SHAPE",
         date=date(2026, 6, 5), image_url="https://images.unsplash.com/photo-1593642531955-b62e17bdaa9c?w=400&h=200&fit=crop&auto=format"),
    dict(title="IAEA Strengthens Radiation Emergency Response After Incident Review",
         summary="Following a comprehensive post-incident review, the IAEA updated Emergency Preparedness and Response protocols with new decontamination benchmarks and improved public communication standards.",
         category=Category.CBRN, source="International Atomic Energy Agency",
         date=date(2026, 5, 28), image_url="https://images.unsplash.com/photo-1628348070889-cb656235b4eb?w=400&h=200&fit=crop&auto=format"),
    dict(title="Industrial Spill Response Delays Multiply Long-Term Ecological Damage",
         summary="Researchers from 12 institutions demonstrate each hour of delayed environmental response to industrial spills multiplies long-term remediation costs by a factor of 3.7, urging new rapid-response protocols.",
         category=Category.ENVIRONMENTAL_SAFETY, source="Journal of Hazardous Materials",
         date=date(2026, 5, 14), image_url="https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?w=400&h=200&fit=crop&auto=format"),
    dict(title="FEMA Deploys AI-Powered Situational Awareness Platform ARIA",
         summary="The Federal Emergency Management Agency launched ARIA, integrating real-time satellite imagery, IoT sensor networks, and predictive modeling for coordinated disaster response operations across the US.",
         category=Category.DISASTER_MEDICINE, source="FEMA",
         date=date(2026, 5, 1), image_url="https://images.unsplash.com/photo-1527515637462-cff94aca3584?w=400&h=200&fit=crop&auto=format"),
    dict(title="OPCW Expands Chemical Detection Training Programme to 40 Nations",
         summary="The Organisation for the Prohibition of Chemical Weapons announced a major expansion of its Laboratory Assistance Programme, providing advanced detection training and equipment to first responders in 40 developing nations.",
         category=Category.CBRN, source="OPCW",
         date=date(2026, 4, 22), image_url="https://images.unsplash.com/photo-1564684006800-aa980ad38e49?w=400&h=200&fit=crop&auto=format"),
]


class Command(BaseCommand):
    help = "Seed the database with initial IRCCP news items (safe to re-run)."

    def handle(self, *args, **options):
        created = 0
        for item in NEWS:
            _, was_created = NewsItem.objects.get_or_create(title=item["title"], defaults=item)
            created += int(was_created)
        self.stdout.write(self.style.SUCCESS(f"Seeded news: {created} created, {len(NEWS) - created} already existed."))
