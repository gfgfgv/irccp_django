from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("publications/", views.publications, name="publications"),
    path("researchers/", views.researchers, name="researchers"),
    path("resources/", views.resources, name="resources"),
    path("journals/", views.journals, name="journals"),
    path("events/", views.events, name="events"),
    path("products/", views.products, name="products"),
    path("upload/", views.upload_publication, name="upload"),
    path("register/", views.register, name="register"),
    path("login/", views.EmailLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("publication/<int:pk>/", views.publication_detail, name="publication_detail"),
    path("publication/<int:pub_id>/comment/", views.add_comment, name="add_comment"),
    path("comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"),
]
