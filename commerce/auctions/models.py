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
    description = models.TextField()
    image_url = models.URLField()
    active = models.BooleanField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    wishers = models.ManyToManyField(User, blank=True, related_name="wishes")
    
    def __str__(self):
        return f"{self.id} {self.title} ({self.active})"

class Bid(models.Model):
    bid = models.FloatField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing2")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user3")


class Comment():
    comment = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing4")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user5")

  

class Wishlist():
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing6")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user7")