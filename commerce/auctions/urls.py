from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category"),
    path("item/<int:item_id>", views.show_item, name="item"),
    path("sell", views.sell, name="sell"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:item_id>", views.add_to_watchlist, name="add_to_watchlist")
]
