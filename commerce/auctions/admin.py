from django.contrib import admin
from .models import AuctionListing, Bid, Comment
# from django.contrib.auth.models import User
# from django.contrib.auth.admin import UserAdmin

# # Register the User model in the admin panel
# admin.site.register(User, UserAdmin)

admin.site.register(AuctionListing)
admin.site.register(Bid)
admin.site.register(Comment)