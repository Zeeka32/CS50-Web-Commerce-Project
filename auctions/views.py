from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from .models import *

def isInWatchList(request, auctionId):
    if request.user.is_authenticated:
        watchList = request.user.watchList
        try:
            watchList.auctions.get(id=auctionId)
            return True
        except:
            return False


def index(request):
    auctions = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {
        "auctions": auctions,
        "message": "Active Listings"
    })


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

        # Attempt to create new user with a watchlist object associated with that user
        try:
            user = User.objects.create_user(username, email, password)
            watchList = WatchList.objects.create(owner = user)
            watchList.save()
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    

@login_required(login_url="login")
def createListing(request):
    if request.method != "POST":
        return render(request, "auctions/listingCreate.html")
    
    title = request.POST["title"]
    description = request.POST["description"]
    startingBid = float(request.POST["startingBid"])
    image = request.POST["picture"]
    category = request.POST["category"]

    if title == "" or description == "" or startingBid <= 0:
        return render(request, "auctions/listingCreate.html", {
            "message": "Invalid input"
        })
    
    auction = AuctionListing.objects.create(title = title, description = description, image = image, category = category,
    author = request.user)

    bid = Bid.objects.create(startingBid = startingBid, highestBid = startingBid, highestBidder = None, auction = auction)

    bid.save()
    auction.save()

    return HttpResponseRedirect(reverse("listing", kwargs={'id':auction.id,}))


def renderListing(request, id):
    auction = AuctionListing.objects.get(pk=id)
    comments = auction.comments.all()
    bidInfo = auction.bid

    onList = isInWatchList(request, auction.id)
    
    return render(request, "auctions/listing.html", {
        "auction": auction,
        "comments": comments,
        "bid" : bidInfo,
        "onWatchList": onList
    })


@login_required(login_url="login")
def addComment(request):
    if request.method == "POST":
        auctionId = request.POST["auctionId"]
        content = request.POST["comment"]
        auction = AuctionListing.objects.get(pk=auctionId)

        if content == "":
            bid = auction.bid
            comments = auction.comments.all()
            return render(request, "auctions/listing.html", {
            "auction": auction,
            "comments": comments,
            "bid":bid,
            "message": "comment can't be empty"
        })

        comment = Comment.objects.create(content = content, commenter = request.user)
        comment.save()
        
        auction.comments.add(comment)

        return HttpResponseRedirect(reverse("listing", kwargs={'id':auction.id,}))
    

@login_required(login_url="login")
def placeBid(request):
    if request.method == "POST":

        bid = request.POST["bid"]
        auctionId = request.POST["auctionId"]

        auction = AuctionListing.objects.get(pk=auctionId)
        bidObject = auction.bid

        if  bid == "" or float(bid) <= bidObject.highestBid:
            comments = auction.comments.all()
            return render(request, "auctions/listing.html", {
                "auction": auction,
                "comments": comments,
                "bid": bidObject,
                "message": "Bid must be larger than the current highest bid"
            })
        
        bidObject.highestBid = bid
        bidObject.bidders += 1
        bidObject.highestBidder = request.user
        bidObject.save()

        return HttpResponseRedirect(reverse("listing", kwargs={'id':auction.id,}))
    

@login_required(login_url="login")
def closeAuction(request):
    auctionId = request.GET["auctionId"]
    auction = AuctionListing.objects.get(pk=auctionId)

    auction.open = False
    auction.save()

    return HttpResponseRedirect(reverse("listing", kwargs={'id':auction.id,}))


@login_required(login_url="login")
def addToWatchList(request):
    auctionId = request.GET["auctionId"]
    watchList = request.user.watchList

    auction = AuctionListing.objects.get(pk=auctionId)

    watchList.auctions.add(auction)
    watchList.save()
        
    return HttpResponseRedirect(reverse("listing", kwargs={'id':auction.id,}))


@login_required(login_url="login")
def removeFromWatchList(request):
    auctionId = request.GET["auctionId"]
    watchList = request.user.watchList

    auction = AuctionListing.objects.get(pk=auctionId)

    watchList.auctions.remove(auction)
        
    return HttpResponseRedirect(reverse("listing", kwargs={'id':auction.id,}))


@login_required(login_url="login")
def renderWatchList(request):
    watchList = request.user.watchList
    auctions = watchList.auctions.all()
    return render(request, "auctions/index.html", {
        "auctions":auctions,
        "message": "Watch List"
    })

def renderCategories(request):
    categories = ["Gaming", "Fashion", "Electronics", "Home", "Toys", "No Category"]
    return render(request, "auctions/categories.html", {
        "categories": categories,
    })


def categoryListing(request, category):
    auctions = AuctionListing.objects.filter(category=category)
    return render(request, "auctions/index.html", {
        "auctions": auctions,
        "message": "Active Listings for " + category
    })
