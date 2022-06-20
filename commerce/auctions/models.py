from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    title = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.title}"


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    starting_price = models.FloatField(default=0)
    active = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    wishers = models.ManyToManyField(User, blank=True, related_name="wishes")
    
    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    bid = models.FloatField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid")

    def __str__(self):
        return f"{self.listing} - {self.bid} - {self.user}"


class Comment():
    comment = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

  

#class Watchlist():
#    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="wishes")
#    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishes")