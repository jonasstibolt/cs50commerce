from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey



# from django.contrib.auth.models import AbstractUser


# class User(AbstractUser):
#     pass


class AuctionListing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_bid = models.DecimalField(max_digits=9, decimal_places=2)
    current_bid = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=4096, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    active = models.BooleanField(default=True)
    end_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Bid(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='bids')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    bid_amount = models.DecimalField(max_digits=9, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.bid_amount}"

class Comment(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.comment[:20]}..."

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    def __str__(self):
        if isinstance(self.content_object, AuctionListing):
            return f"Like on: {self.listing.title} by {self.user.username}."
        elif isinstance(self.content_object, Comment):
            return f"Liked comment: {self.comment.comment[:10]}... on: {self.listing.title} by: {self.user.username}."
        else:
            return f"Like by: {self.user.username} not associated with an object."