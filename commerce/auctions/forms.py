# auctions/forms.py
from django import forms
from .models import AuctionListing, Bid, Comment

class ListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'start_bid', 
                  'image_url',
                  'category', 'end_date']
        widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'category': forms.Select(choices=[('Fashion', 'Fashion'), ('Toys', 'Toys'), ('Electronics', 'Electronics'), ('Home', 'Home')]),
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount']

    def __init__(self, *args, **kwargs):
        self.listing = kwargs.pop('listing', None)  # Accept the listing instance as a parameter
        super(BidForm, self).__init__(*args, **kwargs)

    def clean_bid_amount(self):
        bid_amount = self.cleaned_data.get('bid_amount')

        # Check if the bid amount is less than or equal to 0
        if bid_amount <= 0:
            raise forms.ValidationError("Bid amount must be greater than zero.")

        # Check if the bid amount is less than or equal to the current highest bid
        current_bid = self.listing.current_bid  # Use the listing passed in the form initialization
        if current_bid and bid_amount <= current_bid:
            raise forms.ValidationError("Bid amount must be greater than the current bid made by others.")

        return bid_amount


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']