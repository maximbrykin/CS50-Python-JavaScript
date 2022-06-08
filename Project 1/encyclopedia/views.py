from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from . import util
import markdown2
import random

class CreateNewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput({"class":"form-control"}))
    content = forms.CharField(widget=forms.Textarea({"class":"form-control"}))

# Display the full list of the existing entries.
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Display entry's content.
def entry(request, entry):
    if util.get_entry(entry):
        return render(request, "encyclopedia/entry.html", {
            "entry_content": markdown2.markdown(util.get_entry(entry)),
            "entry_name": entry
         }) 
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry_content": "The requested article on '" + entry +"' does not exist.",
            "entry_name": entry
        })


# Search entries by the form's input.
def search(request):  
    if request.method == "POST":

        # Put a request into q
        q = request.POST.get('q')

        # Redirect if a precise match
        if q in util.list_entries():
            return HttpResponseRedirect(reverse("wiki:entry",args=(q,)))
        
        # Show a list if a partial match 
        elif list(filter(lambda k: q in k, util.list_entries())):
            return render(request, "encyclopedia/search.html", {
                "search_request": q,
                "entries": list(filter(lambda k: q in k, util.list_entries()))
            })
        
        # Show user's query if no coincedence
        else:
            return render(request, "encyclopedia/search.html", {
                "search_request": q
            })

    # Search page without a form input 
    else:
        return render(request, "encyclopedia/search.html")
    

def new(request):
    if request.method == "POST":
        form = CreateNewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title in util.list_entries():
                return render(request, "encyclopedia/new.html", {
                    "error":  '<div class="alert alert-warning">The page with the title "' + title +'" already exists.</div>'               
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("wiki:entry",args=(title,)))
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })
    return render(request, "encyclopedia/new.html", {
        "form": CreateNewPageForm()
    })    


# Edit an entry
def edit_entry(request, entry_name):
    data = {'title': entry_name, 'content': util.get_entry(entry_name)}
    
    if request.method == "POST":
        form = CreateNewPageForm(request.POST)
        if form.is_valid():
            title = request.POST.get('title')
            content = request.POST.get('content')
            util.save_entry(title, bytes(content, 'utf8'))

            # Remove the preceding file if the title has changed
            if title != entry_name:
                util.remove_entry(entry_name)

            return HttpResponseRedirect(reverse("wiki:entry",args=(title,)))
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })

    return render(request, "encyclopedia/edit.html", {
        "form": CreateNewPageForm(initial=data),
        "entry": entry_name
    })


# Show a random entry
def random_entry(request):
    return HttpResponseRedirect(reverse("wiki:entry",args=(random.choice(util.list_entries()),)))