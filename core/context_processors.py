from django.conf import settings

from .models import Category


def category_choices(request):
    return {"CATEGORY_CHOICES": Category.choices}


def donate_url(request):
    return {"DONATE_URL": settings.DONATE_URL}
