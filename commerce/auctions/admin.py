from django.contrib import admin

from .models import Category, Listing, Bid, User, Listing_Comment

# Register your models here.
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(User)
admin.site.register(Listing_Comment)
