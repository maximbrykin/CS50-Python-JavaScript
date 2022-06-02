from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    #path("<str:entry_name>", views.entry, name="entry")
    path("1", views.entry_content, name="entry_content")
]
