
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts/<int:user_id>", views.userposts, name="userposts"),
    path("post/<int:post_id>/set_like", views.set_like, name="set_like"),
    path("allposts", views.allposts, name="allposts"),
    path("save_post", views.save_post, name="save_post"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("profile/<int:user_id>/follow", views.follow, name="follow"),
    path("following_posts", views.following_posts, name="following_posts")
]
