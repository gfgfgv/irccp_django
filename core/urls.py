from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("publications/", views.publications, name="publications"),
    path("researchers/", views.researchers, name="researchers"),
    path("resources/", views.resources, name="resources"),
    path("journals/", views.journals, name="journals"),
    path("upload/", views.upload_publication, name="upload"),
    path("register/", views.register, name="register"),
    path("login/", views.EmailLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
]
