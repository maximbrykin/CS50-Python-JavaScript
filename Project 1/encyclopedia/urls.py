from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
    path("wiki/edit/<str:entry_name>", views.edit_entry, name="edit_entry"),
    path("search", views.search, name="search"),
    path("random", views.random_entry, name="random_entry"),
    path("wiki/<str:entry>", views.entry, name="entry")
]