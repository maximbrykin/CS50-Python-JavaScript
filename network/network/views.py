from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json

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


def allposts (request):
    alltheposts = Post.objects.order_by('-date').all()
    return JsonResponse([post.serialize(request.user) for post in alltheposts], safe=False)


@login_required
def following_posts (request):
    following_users = request.user.followed.all()
    following_posts = Post.objects.filter(author__in=following_users).order_by('-date').all()
    return JsonResponse([post.serialize(request.user) for post in following_posts], safe=False)


@login_required
def follow (request, user_id):
    user = Follower.objects.get(id=user_id)
    if user in request.user.followed.all():
        new_follow_status = False
        user.follow.remove(request.user)
    else:
        new_follow_status = True
        user.follow.add(request.user)
    user.save()
    return JsonResponse({
        "following": new_follow_status,
        "new_followers_num": user.follow.count()
        },
        status=200)


@login_required
def set_like (request, post_id):
    user = Follower.objects.filter(user=request.user).first()
    post = Post.objects.get(id=post_id)
    if post in user.likes.all():
        new_like_status = False
        post.liked.remove(user)
    else:
        new_like_status = True
        post.liked.add(user)
    post.save()
    return JsonResponse({
        "liked": new_like_status,
        "new_like_num": post.liked.count()
        },
        status=200)


def pagination(request, posts):
    posts_list = posts.order_by("-date").all()
    paginator = Paginator(posts_list, 1) # Show 1 post per page.

    #page_number = request.GET.get('page')
    page_number = request.GET['page']
    page_obj = paginator.get_page(page_number)
    return JsonResponse({
        "posts_list": [post.serialize(request.user) for post in page_obj],
        "page_nums": paginator.num_pages
    },
    safe = False)


@login_required 
def save_post(request):
   
    if request.method == "POST":
        form = Post(content=request. POST['new_content'])
        form.author = Follower.objects.get(user=request.user)
        form.save()
    elif request.method == "PUT":
        data = json.loads(request.body)
        id = int(data["id"])
        new_content = data["new_content"]
        post = Post.objects.filter(id=id).first()
        if post.author.user != request.user:
            return HttpResponse(status=401)
        post.content = new_content
        post.save()
        return JsonResponse({
            "result": True
        }, 
        status=200)
    else:
        return JsonResponse({
            "error": f"You cannot modify this post.",
        },
        status = 400)
    return index(request)