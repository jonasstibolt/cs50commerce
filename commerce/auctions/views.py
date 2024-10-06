from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import ListingForm
from django.contrib.auth.decorators import login_required
from .models import User, AuctionListing, Like, Comment
from .forms import BidForm, CommentForm


# def index(request):
#     return render(request, "auctions/index.html")

def index(request):
    listings = AuctionListing.objects.filter(active=True)
    return render(request, 'auctions/index.html', {'listings': listings})

def test_view(request):
    return render(request, 'auctions/test.html')

def error_view(request):
    return render(request, 'auctions/error.html')


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def createListing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user  # Set the current user as the owner
            listing.save()
            print("Form saved succesfully")
            return redirect('index')  # Redirect to a new URL
        else:
            print("Form not saved:", form.error)
    else:
        form = ListingForm()
    return render(request, 'auctions/create_listing.html', {'listing_form': form})

def listing(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)
    
    comments = listing.comments.all()
    bids = listing.current_bid

    if request.method == "POST":
        if 'submit_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            bid_form = BidForm()
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.listing = listing
                new_comment.user = request.user
                new_comment.save()
                return redirect('listing', listing_id=listing.id)
        
        elif 'submit_bid' in request.POST:
            bid_form = BidForm(request.POST, listing=listing)
            comment_form = CommentForm()
            if bid_form.is_valid():
                new_bid = bid_form.save(commit=False)
                new_bid.listing = listing
                new_bid.user = request.user
                new_bid.save()

                listing.current_bid = new_bid.bid_amount
                listing.save()

                print(f"New bid: {listing.current_bid}")
                return redirect('listing', listing_id=listing.id)                 

            if not bid_form.is_valid():
                print(bid_form.errors)

    else:
        comment_form = CommentForm()
        bid_form = BidForm(listing=listing)
        


    
    return render(request, 'auctions/listing.html', 
              {'listing': listing, 
              'comments': comments, 
              'comment_form': comment_form, 
              'bid_form': bid_form,
              'bids' : bids,}
              )


# def like(request, content_type, object_id):

#     user = request.user
#     like, created = Like.objects.get_or_create(user=user, content_type=content_type, id=object_id)

#     if content_type == AuctionListing:
#         content_object = get_object_or_404(AuctionListing, id=object_id)
#     elif content_type == Comment:
#         content_object = get_object_or_404(Comment, id=object_id)
#     else:
#         return redirect('error')
    

#     if created:

