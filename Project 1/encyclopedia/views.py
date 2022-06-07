from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.db.models.functions import Substr, Lower, StrIndex
from . import util
import markdown2


# Display the full list of the existing entries.
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Display entry's content.
def entry_content(request, entry_name):
    if util.get_entry(entry_name):
        return render(request, "encyclopedia/entry.html", {
            "entry_content": markdown2.markdown(util.get_entry(entry_name)),
            "entry_name": entry_name
         }) 
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry_content": "The requested article on '" + entry_name +"' does not exist.",
            "entry_name": entry_name
        })


# Search entries by the form's input.
def search(request):  
    if request.method == "POST":

        # Put a request into q
        q = request.POST.get('q')

        # Put a filtered list into l
        l = list(filter(lambda k: q in k, util.list_entries()))

        # Redirect if a precise match
        if q in util.list_entries():
            return HttpResponseRedirect(reverse("wiki:url_name",args=(q,)))
        
        # Show a list if a partial match 
        elif l:
            return render(request, "encyclopedia/search.html", {
                "search_request": q,
                "entries": l
            })
        
        # Show user's query if no coincedence
        else:
            return render(request, "encyclopedia/search.html", {
                "search_request": q
            })

    # Search page without a form request 
    else:
        return render(request, "encyclopedia/search.html")
    

def random_content(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def new_content(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


 