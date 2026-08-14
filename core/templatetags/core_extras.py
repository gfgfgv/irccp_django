from django import template
from django.utils.safestring import mark_safe

from core.models import BADGE_COLORS, CATEGORY_CONFIG, get_badge

register = template.Library()

# Minimal hand-drawn line-icon set (generic shapes, not copied from any icon
# library) used across the templates in place of the original lucide-react
# icons.
_ICONS = {
    "search": '<circle cx="10" cy="10" r="6"/><line x1="20" y1="20" x2="14.5" y2="14.5"/>',
    "menu": '<line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>',
    "x": '<line x1="5" y1="5" x2="19" y2="19"/><line x1="19" y1="5" x2="5" y2="19"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 20c0-4.4 3.6-7 8-7s8 2.6 8 7"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c0-3.6 2.9-6 6.5-6s6.5 2.4 6.5 6"/><circle cx="17" cy="9" r="2.8"/><path d="M15.5 14c2.9.3 5 2.4 5 6"/>',
    "logout": '<path d="M9 4H5a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h4"/><line x1="21" y1="12" x2="9" y2="12"/><polyline points="16 7 21 12 16 17"/>',
    "award": '<circle cx="12" cy="8" r="6"/><path d="M8.5 13.5 6.5 21l5.5-3 5.5 3-2-7.5"/>',
    "book": '<path d="M4 5.5C4 4.7 4.7 4 5.5 4H12v16H5.5A1.5 1.5 0 0 1 4 18.5z"/><path d="M20 5.5C20 4.7 19.3 4 18.5 4H12v16h6.5a1.5 1.5 0 0 0 1.5-1.5z"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><line x1="3" y1="12" x2="21" y2="12"/>',
    "upload": '<path d="M12 16V4"/><polyline points="7 9 12 4 17 9"/><path d="M4 16v3a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-3"/>',
    "external": '<path d="M14 4h6v6"/><line x1="20" y1="4" x2="11" y2="13"/><path d="M18 13v6a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h6"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="1.5"/><path d="M3.5 6.5 12 13l8.5-6.5"/>',
    "phone": '<path d="M6 3h3l1.5 4.5-2 1.5a12 12 0 0 0 6.5 6.5l1.5-2 4.5 1.5v3a1.5 1.5 0 0 1-1.6 1.5A16.5 16.5 0 0 1 4.5 4.6 1.5 1.5 0 0 1 6 3z"/>',
    "building": '<rect x="5" y="3" width="10" height="18"/><rect x="15" y="9" width="5" height="12"/><line x1="8" y1="7" x2="8" y2="7.01"/><line x1="12" y1="7" x2="12" y2="7.01"/><line x1="8" y1="11" x2="8" y2="11.01"/><line x1="12" y1="11" x2="12" y2="11.01"/><line x1="8" y1="15" x2="8" y2="15.01"/><line x1="12" y1="15" x2="12" y2="15.01"/>',
    "chevron-right": '<polyline points="9 5 16 12 9 19"/>',
    "flame": '<path d="M12 3c1 3-3 4-3 8a3 3 0 0 0 6 0c0-1.5-1-2-1-3.5 2 1.5 3 3.5 3 5.5a5 5 0 0 1-10 0c0-4 3-5.5 5-10z"/>',
    "shield": '<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/>',
    "zap": '<polygon points="13 2 4 14 11 14 10 22 20 9 13 9 13 2"/>',
    "heart": '<path d="M12 20s-7-4.5-9.3-8.8C1.2 8 2.7 5 5.8 5c1.8 0 3.3 1 4.2 2.5C11 6 12.4 5 14.2 5c3.1 0 4.6 3 3.1 6.2C19.9 15.5 12 20 12 20z"/>',
    "leaf": '<path d="M5 20C5 10 12 4 20 4c0 8-6 15-16 15z"/><path d="M5 20c1-4 3-7 7-9.5"/>',
    "plus": '<line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>',
    "arrow-right": '<line x1="4" y1="12" x2="20" y2="12"/><polyline points="14 6 20 12 14 18"/>',
    "check": '<polyline points="4 12 9 18 20 6"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 16 14"/>',
    "newspaper": '<rect x="3" y="5" width="13" height="15" rx="1"/><path d="M16 9h4v9a2 2 0 0 1-2 2h-2"/><line x1="6" y1="9" x2="13" y2="9"/><line x1="6" y1="12.5" x2="13" y2="12.5"/><line x1="6" y1="16" x2="11" y2="16"/>',
    "camera": '<path d="M4 8h3l1.5-2h7L17 8h3a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z"/><circle cx="12" cy="13" r="3.5"/>',
    "image": '<rect x="3" y="4" width="18" height="16" rx="1.5"/><circle cx="8.5" cy="9.5" r="1.5"/><path d="M21 16l-5-5-9 9"/>',
    "filter": '<polygon points="4 4 20 4 14 12.5 14 19 10 21 10 12.5"/>',
}


@register.simple_tag
def icon(name, size=16, cls=""):
    body = _ICONS.get(name, "")
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round" class="icon {cls}">{body}</svg>'
    )
    return mark_safe(svg)


@register.simple_tag
def cat_icon(category, size=16, cls=""):
    """Render the logo uploaded for this category (via /admin/) at large
    enough sizes, or the built-in inline-SVG icon otherwise.

    Small raster logos (chips, filter pills) turn into an illegible blur, so
    below MIN_LOGO_SIZE we always use the crisp vector icon instead — even
    if a logo has been uploaded — and only switch to the real logo once
    there's enough room to actually see it (category cards, hero, navbar).
    """
    MIN_LOGO_SIZE = 20

    cfg = CATEGORY_CONFIG.get(category, {})
    if size < MIN_LOGO_SIZE:
        return icon(cfg.get("icon", ""), size, cls)

    from django.core.cache import cache

    from core.models import CategoryLogo

    cache_key = f"cat_logo_url__{category}".replace(" ", "_")
    url = cache.get(cache_key, "")
    if not url:
        logo = CategoryLogo.objects.filter(category=category).first()
        url = logo.image.url if logo and logo.image else ""
        cache.set(cache_key, url, 300)

    if url:
        return mark_safe(
            f'<img src="{url}" alt="{category}" class="cat-logo-img {cls}" '
            f'style="width:{size}px;height:{size}px;object-fit:contain;flex-shrink:0;display:inline-block;">'
        )

    return icon(cfg.get("icon", ""), size, cls)


@register.simple_tag
def site_logo():
    """URL of the uploaded main IRCCP shield logo, or '' if none uploaded yet."""
    from django.core.cache import cache

    from core.models import SiteBranding

    url = cache.get("site_logo_url", "")
    if not url:
        branding = SiteBranding.objects.first()
        url = branding.image.url if branding and branding.image else ""
        cache.set("site_logo_url", url, 300)
    return url


@register.simple_tag
def cat_config(category, key):
    cfg = CATEGORY_CONFIG.get(category, {})
    return cfg.get(key, "")


@register.simple_tag
def badge_for(count):
    return get_badge(count)


@register.simple_tag
def badge_color(tier, key):
    return BADGE_COLORS.get(tier, {}).get(key, "")


@register.filter
def split_first(value):
    """Return the first word of a name, e.g. for greeting 'Jane Doe' -> 'Jane'."""
    return (value or "").split(" ")[0]
