
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts/<int:user_id>", views.userposts, name="userposts"),
    path("allposts", views.allposts, name="allposts"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("following_posts", views.following_posts, name="following_posts")
]
