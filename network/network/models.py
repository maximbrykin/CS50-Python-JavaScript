from tkinter import CASCADE
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Follower(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follow = models.ManyToManyField(User, blank=True, related_name="followed")
    mood = models.CharField(blank=True, max_length=64)
    def serialize(self, user):
        return {
            "user_id": self.user.id,
            "username": self.user.username,
            "mood": self.mood,
            "followed_by_num": self.follow.count(),
            "follows_num": self.user.followed.count(),
            "is_following":  (not user.is_anonymous) and self in user.followed.all(),
            "can_follow": (not user.is_anonymous) and self.user != user
        }
    def __str__(self):
        followers = ""
        for follower in self.follow.all():
            followers += " " + follower.username
        return f"{self.user.username} - id:{self.user.id} - follows: {followers}"


class Post(models.Model):
    content = models.CharField(max_length=512)
    author = models.ForeignKey(Follower, on_delete=models.CASCADE, related_name="posts")
    liked = models.ManyToManyField(Follower, blank=True, related_name="likes")
    date = models.DateTimeField(default=timezone.now)
    def serialize(self, user):
        return {
            "id": self.id,
            "content": self.content,
            "date": self.date.strftime("%b %#d %Y, %#I:%M %p"),
            "author_id": self.author.id,
            "author": self.author.user.username,
            "likes": self.liked.count(),
            #"liked": self in Follower.objects.filter(user=user).first().likes().all() and (not user.is_anonymous),
            "can_edit": self.author.user == user
        }
    def __str__(self):
            return f"{self.content} - {self.date} - {self.author} - likes: {self.liked.count()}"