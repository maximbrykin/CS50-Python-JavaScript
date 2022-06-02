from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_content(request, entry_name):
    return render(request, "encyclopedia/entry.html", {
        "entry_content": markdown2.markdown(util.get_entry(entry_name))
    })