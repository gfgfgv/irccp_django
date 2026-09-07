import random

from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from .forms import EmailLoginForm, PublicationUploadForm, RegisterForm
from .models import CATEGORY_CONFIG, Category, Company, Event, Journal, NewsItem, Publication, Researcher, Resource


def _top_and_rest(items, top_count=4, rest_count=4):
    """Split a list into a (top, rest) pair for the News-style card+row layout."""
    return items[:top_count], items[top_count:top_count + rest_count]


def home(request):
    publications_list = list(Publication.objects.select_related("author__user")[:8])
    researchers_list = list(Researcher.objects.select_related("user").prefetch_related("publications")[:8])
    news_list = list(NewsItem.objects.all()[:8])
    # Events: show upcoming ones first (soonest first); if there aren't 8
    # upcoming, fill the rest with the most recent past events so the
    # section isn't awkwardly empty right after a real event happens.
    from django.utils.timezone import localdate
    today = localdate()
    upcoming_events = list(Event.objects.filter(date__gte=today).order_by("date"))
    if len(upcoming_events) < 8:
        past_events = list(Event.objects.filter(date__lt=today).order_by("-date")[:8 - len(upcoming_events)])
        events_list = upcoming_events + past_events
    else:
        events_list = upcoming_events[:8]

    # Resources/Journals/Companies don't have a "recent" concept, so we just
    # show a random sample each time rather than pretending to rank them.
    all_resources = list(Resource.objects.all())
    all_journals = list(Journal.objects.all())
    all_companies = list(Company.objects.all())
    resources_list = random.sample(all_resources, min(8, len(all_resources)))
    journals_list = random.sample(all_journals, min(8, len(all_journals)))
    companies_list = random.sample(all_companies, min(8, len(all_companies)))

    pub_top, pub_rest = _top_and_rest(publications_list)
    res_top, res_rest = _top_and_rest(researchers_list)
    resc_top, resc_rest = _top_and_rest(resources_list)
    jour_top, jour_rest = _top_and_rest(journals_list)
    news_top, news_rest = _top_and_rest(news_list)
    event_top, event_rest = _top_and_rest(events_list)
    company_top, company_rest = _top_and_rest(companies_list)

    context = {
        "publications_top": pub_top,
        "publications_rest": pub_rest,
        "researchers_top": res_top,
        "researchers_rest": res_rest,
        "resources_top": resc_top,
        "resources_rest": resc_rest,
        "journals_top": jour_top,
        "journals_rest": jour_rest,
        "news_top": news_top,
        "news_rest": news_rest,
        "events_top": event_top,
        "events_rest": event_rest,
        "companies_top": company_top,
        "companies_rest": company_rest,
        "categories": category_cards(),
        "stats": {
            "publications": Publication.objects.count(),
            "categories": len(Category.choices),
            "journals": Journal.objects.count(),
            "resources": Resource.objects.count(),
        },
    }
    return render(request, "core/home.html", context)


def category_cards():
    cards = []
    for value, label in Category.choices:
        cfg = CATEGORY_CONFIG[value]
        cards.append({
            "value": value,
            "label": label,
            "hex": cfg["hex"],
            "bg": cfg["bg"],
            "icon": cfg["icon"],
            "desc": cfg["desc"],
            "count": Publication.objects.filter(category=value).count(),
        })
    return cards


def publications(request):
    qs = Publication.objects.select_related("author__user")
    query = request.GET.get("q", "").strip()
    cat = request.GET.get("cat", "").strip()

    if cat:
        qs = qs.filter(category=cat)
    if query:
        qs = qs.filter(
            Q(title__icontains=query)
            | Q(abstract__icontains=query)
            | Q(author__user__first_name__icontains=query)
            | Q(author__user__last_name__icontains=query)
        )

    context = {
        "publications": qs,
        "query": query,
        "active_cat": cat,
        "categories": Category.choices,
        "category_config": CATEGORY_CONFIG,
        "total_count": Publication.objects.count(),
    }
    return render(request, "core/publications.html", context)


def researchers(request):
    qs = Researcher.objects.select_related("user").prefetch_related("publications")
    query = request.GET.get("q", "").strip()
    if query:
        qs = qs.filter(
            Q(user__first_name__icontains=query)
            | Q(user__last_name__icontains=query)
            | Q(workplace__icontains=query)
            | Q(interests__icontains=query)
        )
    context = {
        "researchers": qs,
        "query": query,
        "total_count": Researcher.objects.count(),
    }
    return render(request, "core/researchers.html", context)


def resources(request):
    cat = request.GET.get("cat", "").strip()
    qs = Resource.objects.all()
    if cat:
        qs = qs.filter(category=cat)
    context = {"resources": qs, "active_cat": cat, "categories": Category.choices,
               "category_config": CATEGORY_CONFIG}
    return render(request, "core/resources.html", context)


def journals(request):
    cat = request.GET.get("cat", "").strip()
    qs = Journal.objects.all()
    if cat:
        qs = qs.filter(category=cat)
    context = {"journals": qs, "active_cat": cat, "categories": Category.choices,
               "category_config": CATEGORY_CONFIG}
    return render(request, "core/journals.html", context)


def events(request):
    cat = request.GET.get("cat", "").strip()
    qs = Event.objects.all()
    if cat:
        qs = qs.filter(category=cat)
    context = {"events": qs, "active_cat": cat, "categories": Category.choices,
               "category_config": CATEGORY_CONFIG}
    return render(request, "core/events.html", context)


def products(request):
    cat = request.GET.get("cat", "").strip()
    qs = Company.objects.all()
    if cat:
        qs = qs.filter(category=cat)
    context = {"companies": qs, "active_cat": cat, "categories": Category.choices,
               "category_config": CATEGORY_CONFIG}
    return render(request, "core/products.html", context)


class EmailLoginView(LoginView):
    template_name = "core/login.html"
    authentication_form = EmailLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return self.request.GET.get("next") or reverse_lazy("core:home")


def logout_view(request):
    auth_logout(request)
    return redirect("core:home")


def register(request):
    if request.user.is_authenticated:
        return redirect("core:home")
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, f"Welcome to IRCCP, {user.first_name}! You can now upload publications.")
            return redirect("core:home")
    else:
        form = RegisterForm()
    return render(request, "core/register.html", {"form": form})


@login_required(login_url="core:login")
def upload_publication(request):
    # Если у пользователя нет Researcher, создаем его автоматически
    researcher, created = Researcher.objects.get_or_create(
        user=request.user,
        defaults={
            "degree": "Researcher",
            "workplace": "Independent Researcher"
        }
    )

    if request.method == "POST":
        form = PublicationUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pub = form.save(commit=False)
            pub.author = researcher
            pub.save()
            messages.success(request, "Your publication has been added to the IRCCP database.")
            return redirect("core:publications")
    else:
        form = PublicationUploadForm()
    return render(request, "core/upload.html", {"form": form})
