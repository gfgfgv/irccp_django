from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.urls import reverse


class Category(models.TextChoices):
    FIRE_SAFETY = "Fire Safety", "Fire Safety"
    CBRN = "CBRN", "CBRN"
    EOD = "EOD", "EOD"
    DISASTER_MEDICINE = "Disaster Medicine", "Disaster Medicine"
    ENVIRONMENTAL_SAFETY = "Environmental Safety", "Environmental Safety"


CATEGORY_CONFIG = {
    Category.FIRE_SAFETY: {
        "hex": "#C73B0F", "bg": "#FFF4F0", "icon": "flame",
        "desc": "Fire prevention, suppression technologies, evacuation systems, and rescue operations in all environments.",
    },
    Category.CBRN: {
        "hex": "#1B6B35", "bg": "#F0FFF4", "icon": "shield",
        "desc": "Chemical, Biological, Radiological, and Nuclear defence — detection, protection, and decontamination.",
    },
    Category.EOD: {
        "hex": "#7B2D00", "bg": "#FFF8F0", "icon": "zap",
        "desc": "Explosive Ordnance Disposal: techniques, robotic systems, IED defeat, and post-conflict mine action.",
    },
    Category.DISASTER_MEDICINE: {
        "hex": "#1352A0", "bg": "#EFF6FF", "icon": "heart",
        "desc": "Mass casualty management, emergency healthcare, field surgery, and medical resilience in disasters.",
    },
    Category.ENVIRONMENTAL_SAFETY: {
        "hex": "#0E7490", "bg": "#F0FFFE", "icon": "leaf",
        "desc": "Industrial spill response, environmental hazard assessment, monitoring, and ecological protection.",
    },
}

BADGE_COLORS = {
    "gold": {"bg": "#FBF0D0", "text": "#7C5200", "border": "#D4A830"},
    "silver": {"bg": "#EEF0F5", "text": "#374060", "border": "#8E9AB5"},
    "bronze": {"bg": "#FBF0EB", "text": "#7A3A1A", "border": "#C4845A"},
}


def get_badge(count: int):
    if count >= 9:
        return {"label": "Member of Scientific Committee", "tier": "gold"}
    if count >= 3:
        return {"label": "Senior Researcher", "tier": "silver"}
    if count >= 1:
        return {"label": "Researcher", "tier": "bronze"}
    return None


class Researcher(models.Model):
    """Extended profile for a registered researcher, one-to-one with Django's User."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="researcher")
    workplace = models.CharField("Place of work / institution", max_length=255, blank=True)
    interests = models.TextField("Scientific interests", blank=True)
    phone = models.CharField("Phone number", max_length=50, blank=True)
    photo = models.ImageField("Profile photo", upload_to="avatars/", blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-joined_at"]

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    @property
    def name(self):
        return self.user.get_full_name() or self.user.username

    @property
    def publication_count(self):
        return self.publications.count()

    @property
    def badge(self):
        return get_badge(self.publication_count)

    def get_absolute_url(self):
        return reverse("core:researchers")


class Publication(models.Model):
    title = models.CharField(max_length=500)
    abstract = models.TextField()
    category = models.CharField(max_length=32, choices=Category.choices)
    author = models.ForeignKey(Researcher, on_delete=models.CASCADE, related_name="publications")
    doi = models.CharField("DOI or URL", max_length=500, blank=True)
    file = models.FileField("Publication file (PDF)", upload_to="publications/", blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title

    @property
    def institution(self):
        return self.author.workplace


class NewsItem(models.Model):
    title = models.CharField(max_length=500)
    summary = models.TextField()
    category = models.CharField(max_length=32, choices=Category.choices)
    source = models.CharField(max_length=255)
    date = models.DateField()
    image = models.ImageField(upload_to="news/", blank=True, null=True)
    image_url = models.URLField("External image URL (used if no image uploaded)", blank=True)
    source_url = models.URLField("Original article URL", blank=True, unique=False,
                                  help_text="Used to avoid importing the same RSS item twice.")
    is_auto_imported = models.BooleanField(default=False, help_text="True if this item came from the RSS auto-fetch job.")

    class Meta:
        ordering = ["-date"]
        verbose_name = "News item"
        verbose_name_plural = "News items"

    def __str__(self):
        return self.title

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        return self.image_url


class CategoryLogo(models.Model):
    """Custom logo image uploaded per research category, editable from /admin/.

    Falls back to the built-in inline-SVG icon (see core_extras.cat_icon)
    wherever no logo has been uploaded for a category yet.
    """

    category = models.CharField(max_length=32, choices=Category.choices, unique=True)
    image = models.ImageField("Logo image", upload_to="category_logos/")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category logo"
        verbose_name_plural = "Category logos"
        ordering = ["category"]

    def __str__(self):
        return self.get_category_display()


class SiteBranding(models.Model):
    """The main IRCCP shield logo shown in the navbar and hero section.

    Singleton-style: saving a new one automatically replaces the previous
    row, so there's always at most one active site logo.
    """

    image = models.ImageField("Site logo", upload_to="branding/")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site logo"
        verbose_name_plural = "Site logo"

    def __str__(self):
        return "IRCCP site logo"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        SiteBranding.objects.exclude(pk=self.pk).delete()


@receiver([post_save, post_delete], sender=CategoryLogo)
def _clear_category_logo_cache(sender, instance, **kwargs):
    cache.delete(f"cat_logo_url__{instance.category}".replace(" ", "_"))


@receiver([post_save, post_delete], sender=SiteBranding)
def _clear_site_logo_cache(sender, **kwargs):
    cache.delete("site_logo_url")
