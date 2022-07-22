from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User, Post, Follower



def index(request):
    return render(request, "network/index.html")


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def userposts (request, user_id):
    posts = Post.objects.filter(author_id=user_id).order_by('-date')
    return JsonResponse([post.serialize(request.user) for post in posts], safe=False)


def profile (request, user_id):
    profile = Follower.objects.filter(id=user_id).first()
    return JsonResponse(profile.serialize(request.user), status=200)


@login_required(login_url='/login')
def following_posts (request):
    following_users = request.user.followed.all()
    following_posts = Post.objects.filter(author__in=following_users).order_by('-date').all()
    return JsonResponse([post.serialize(request.user) for post in following_posts], safe=False)
    '''return render (request, "network/index.html", {
                "vari": following_users
            })'''

def allposts (request):
    alltheposts = Post.objects.order_by('-date').all()
    return JsonResponse([post.serialize(request.user) for post in alltheposts], safe=False)