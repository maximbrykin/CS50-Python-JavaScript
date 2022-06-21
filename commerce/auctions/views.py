from logging import exception
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Category, Listing, Bid, Listing_Comment


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
def show_item(request, item_id, **kwargs):
    item = Listing.objects.get(pk=item_id)
    fa_style = "fa-regular"
    button_class = ''
    message = ''
    message_class = ''
    comment_button_class = ''

    # Show authorized content
    if request.user.is_authenticated:
        # Style a watchlist icon depending on the listings status
        if request.user in item.wishers.all():
            fa_style = "fa-solid"
        # Show Sell button to the listing's owner
        if item.owner == request.user:
            button_class = "show"
        comment_button_class = "show"
        # Show congratulations!
        if not item.active and item.owner == bid.user and item.owner == request.user:
            message = "Congratulations! Your are the winner."
            message_class = "alert-success show"

    # Show the latest bid
    try:
        bid = Bid.objects.filter(listing=item).last()
    # If there are no bids - add the first bid equal to the starting price    
    except ObjectDoesNotExist:
        init_bid = Bid.objects.create(bid=item.starting_price, listing=item, user=item.owner)
        init_bid.save()
        bid = Bid.objects.get(pk=item_id)

    # Show comments
    comments = Listing_Comment.objects.filter(listing=item)         

    # Show the listing page
    return render(request, "auctions/item.html",{
        "item": item,
        "bid": bid,
        "fa_style": fa_style,
        "message": message,
        "message_class": message_class,
        "button_class": button_class,
        "comments": comments,
        "comment_button_class": comment_button_class
    })


def place_bid(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            item_id = int(request.POST["listing_id"])
            item = Listing.objects.get(pk=int(request.POST["listing_id"]))
            bid = Bid.objects.filter(listing=item).last()
            # post = request.POST[]

            # Place a bid
            try:
                new_bid = float(request.POST["bid"])
            except ValueError:
                return HttpResponseRedirect(reverse("item",args=(item_id,)))
                #, kwargs={
                #    "message": "Input a correct bid.",
                #    "class": "alert-danger show"
                #}))
            if not item.active:
                return HttpResponseRedirect(reverse("item",args=(item_id,)))
            elif (new_bid > bid.bid) or ((new_bid == item.starting_price) and (item.owner == bid.user)):
                add_bid = Bid.objects.create(bid=new_bid, listing=item, user=request.user)
                add_bid.save()
                return HttpResponseRedirect(reverse("item",args=(item_id,)))
                #return render(request, "auctions/item.html", {
                #    "message": "Your bid has been set as the current bid = $" + str(new_bid),
                #    "class": "alert-primary show"
                #})
            else:
                request.session['message'] = "Increase your bid."
                request.session['class'] = "alert-warning show"
                #return HttpResponseRedirect(reverse("item",args=(item_id,)))
                #kwargs = {"arg1" : "Geeks", "arg2" : "for", "arg3" : "Geeks"}
                return HttpResponseRedirect(reverse("item",args=(item_id,)))
    
    return HttpResponseRedirect(reverse("item",args=(item_id,)))


def sell(request):
    if request.method == "POST":
        item_id = int(request.POST["listing_id"])

        if request.user.is_authenticated:
            item = Listing.objects.get(pk=item_id)
            bid = Bid.objects.filter(listing=item).last() 
            if item.owner == request.user:
                if item.active: 
                    item.active = False
                    item.owner = bid.user
                else:
                    item.active = True
                item.save()
            return HttpResponseRedirect(reverse("item",args=(item_id,)))
        return HttpResponseRedirect(reverse("login"))
    return HttpResponseRedirect(reverse("index"))

    '''
        return render(request, "auctions/item.html", {
            "message": "Your've sold this listing.",
            "class": "alert-success show"
        })
    '''

@login_required(login_url='/login')
def watchlist(request):
    listings = Listing.objects.filter(wishers=request.user)
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


@login_required(login_url='/login')
def add_to_watchlist(request, item_id):
    item = Listing.objects.get(pk=item_id)
    if request.user in item.wishers.all():
        item.wishers.remove(request.user)
    else:
        item.wishers.add(request.user)
    item.save()
    message = "DONE!"
    notification(request,message)
    return HttpResponseRedirect(reverse("item",args=(item_id,)))


def post_comment(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            item_id = int(request.POST["listing_id"])
            item = Listing.objects.get(pk=item_id)
            comment = request.POST["comment"]
            if comment:
                add_comment = Listing_Comment.objects.create(comment=comment, listing=item, user=request.user)
                add_comment.save()
            return HttpResponseRedirect(reverse("item",args=(item_id,)))    
        else:
            return HttpResponseRedirect(reverse("login"))


def notification(request,message):
    return render(request, "auctions/notifications.html", {
        "message": message,
        "back_url": "#"
    })
    return HttpResponseRedirect(reverse("item",args=(item_id,)))
    