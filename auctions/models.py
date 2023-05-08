from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    
class WatchList(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="watchList")
    auctions = models.ManyToManyField("auctions.AuctionListing")

    def __str__(self):
        return f"{self.owner}'s watchlist"

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    bidders = models.IntegerField(default=0)
    startingBid = models.FloatField()
    highestBid = models.FloatField()
    highestBidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    auction = models.OneToOneField("auctions.AuctionListing", on_delete=models.CASCADE, related_name="bid", blank=True, null=True)

    def __str__(self):
        return f"highest bid placed by {self.highestBidder} and its value is {self.highestBid}$ for {self.auction.title}"


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=1024)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    auction = models.ManyToManyField("auctions.AuctionListing", related_name="comments")
    date_created = models.DateField(auto_now=True)

    def __str__(self):
        return f"commented created by {self.commenter} on {self.date_created}"


class AuctionListing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1024)
    image = models.CharField(max_length=1024, blank=True)
    category = models.CharField(max_length=255, blank=True)
    date = models.DateField(auto_now=True)
    open = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")

    def __str__(self):
        return f"Auction for {self.title} placed by {self.author}"
