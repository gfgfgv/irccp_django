from django.contrib import admin

from .models import CategoryLogo, NewsItem, Publication, Researcher, SiteBranding


@admin.register(Researcher)
class ResearcherAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "workplace", "publication_count", "joined_at")
    search_fields = ("user__first_name", "user__last_name", "user__email", "workplace")


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "uploaded_at")
    list_filter = ("category",)
    search_fields = ("title", "abstract")


@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "source", "date", "is_auto_imported")
    list_filter = ("category", "is_auto_imported", "source")
    search_fields = ("title", "summary", "source")


@admin.register(CategoryLogo)
class CategoryLogoAdmin(admin.ModelAdmin):
    list_display = ("category", "image", "updated_at")


@admin.register(SiteBranding)
class SiteBrandingAdmin(admin.ModelAdmin):
    list_display = ("__str__", "image", "updated_at")

    def has_add_permission(self, request):
        # Singleton: only allow adding a new logo if none exists yet.
        # To change the logo, edit the existing row instead.
        return not SiteBranding.objects.exists()
