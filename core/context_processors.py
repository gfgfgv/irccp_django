from .models import Category


def category_choices(request):
    return {"CATEGORY_CHOICES": Category.choices}
