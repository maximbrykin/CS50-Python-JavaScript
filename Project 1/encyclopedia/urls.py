from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("new-entry", views.new_content, name="new-entry"),
    path("search", views.search, name="search"),
    path("random-entry", views.random_content, name="random-entry"),
    path("wiki/<str:entry_name>", views.entry_content, name="url_name")
]
