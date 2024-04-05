# auctions/forms.py
from django import forms
from .models import AuctionListing

class ListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'start_bid', 'image_url', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'category': forms.Select(choices=[('Fashion', 'Fashion'), ('Toys', 'Toys'), ('Electronics', 'Electronics'), ('Home', 'Home')]),
        }