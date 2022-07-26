
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.posts, name="posts"),
    path("posts/<int:user_id>", views.userposts, name="userposts"),
    path("posts/following", views.following_posts, name="following_posts"),
    path("save_post", views.save_post, name="save_post"),
    path("post/<int:post_id>/set_like", views.set_like, name="set_like"),
    path("following_posts", views.following_posts, name="following_posts"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("profile/<int:user_id>/follow", views.follow, name="follow")
]
