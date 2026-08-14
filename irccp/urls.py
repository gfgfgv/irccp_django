from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve as static_serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]

# Media (user uploads) is served by Django itself even outside DEBUG. This
# isn't ideal at real scale, but is perfectly fine for a small/free
# deployment — WhiteNoise (in settings.py MIDDLEWARE) handles static files
# in production instead, so only media needs this fallback.
#
# NOTE: Django's usual `static()` helper silently does nothing when
# DEBUG=False, so we call the underlying view directly instead.
urlpatterns += [
    re_path(r"^media/(?P<path>.*)$", static_serve, {"document_root": settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
