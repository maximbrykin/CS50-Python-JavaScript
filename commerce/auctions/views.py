from logging import exception
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Count

from .models import User, Category, Listing, Bid, Comment, Wishlist

#@login_required(login_url='/login')

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


def login_view(request):
    
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# Categories List Page
def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })


# Category Page
def category(request, category_id):
    category = Category.objects.get(pk=category_id)
    return render(request, "auctions/category.html", {
        "category": category.title,
        "listings": category.listings.all()
    })


# Item Page
def item(request, item_id):
    item = Listing.objects.get(pk=item_id)
    
    # If there are no bids - add the first bid equal to the starting price
    try:
        bid = Bid.objects.filter(listing=item).order_by("bid").last()    
    except ObjectDoesNotExist:
        init_bid = Bid.objects.create(bid=item.starting_price, listing=item, user=item.owner)
        init_bid.save()
        bid = Bid.objects.get(pk=item_id)

    # Show congratulations
    if not item.active and item.owner == request.user:
        return render(request, "auctions/item.html", {
                    "message": "Congratulations! Your are the winner for this listing.",
                    "class": "alert-primary show"
                })

    # Place a bid
    if request.method == "POST":
        if request.user.is_authenticated:
            try:
                new_bid = float(request.POST["bid"])
            except ValueError:
                return HttpResponseRedirect(reverse("item",args=(item_id,)))
                #, kwargs={
                #    "message": "Input a correct bid.",
                #    "class": "alert-danger show"
                #}))
            if item.active == False:
               return HttpResponseRedirect(reverse("item",args=(item_id,)))
            elif new_bid > bid.bid:
                add_bid = Bid.objects.create(bid=new_bid, listing=item, user=request.user) #request.POST["participant"]")
                add_bid.save()
                return HttpResponseRedirect(reverse("item",args=(item_id,)))
                #return render(request, "auctions/item.html", {
                #    "message": "Your bid has been set as the current bid = $" + str(new_bid),
                #    "class": "alert-primary show"
                #})
            else:
                return render(request, "auctions/item.html", {
                    "message": "Increase your bid.",
                    "class": "alert-warning show"
                })
        else:
            return HttpResponseRedirect(reverse("login"))
    return render(request, "auctions/item.html",{
        "item": item,
        "bid": bid
    })


def sell(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            item_id = int(request.POST["listing_id"])
            item = Listing.objects.get(pk=item_id)
            
            if item.owner == request.user:
                if item.active: 
                    item.active = False
                    item.owner = request.user
                else:
                    item.active = True
                    item.save()
        return HttpResponseRedirect(reverse("item",args=(item_id,)))

    return HttpResponseRedirect(reverse("index"))

    '''
        return render(request, "auctions/item.html", {
            "message": "Your've sold this listing.",
            "class": "alert-success show"
        })
    '''