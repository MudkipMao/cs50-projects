from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Watchlist (M2M)
    watched_listings = models.ManyToManyField(
        'Auction',
        related_name="users_watching",
        blank=True,
    )
    pass


class Auction(models.Model):
    # User
    submitter = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name="user_listings"
    )
    # Title
    title = models.CharField(max_length=64)
    # Description
    description = models.CharField(max_length=200)
    # Starting price
    starting_price = models.DecimalField(max_digits=8, decimal_places=2)
    # URL for image (optional)
    image = models.ImageField(blank=True, null=True)
    # Category
    category = models.CharField(max_length=64)
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    # Winner (blank to start)
    winner = models.ForeignKey(
        'User',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="user_wins"
    )
    pass


class Bid(models.Model):
    # User (foreign)
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name="user_bids"
    )
    # Price
    bid_price = models.DecimalField(max_digits=8, decimal_places=2)
    # Auction (foreign)
    auction = models.ForeignKey(
        'Auction',
        on_delete=models.CASCADE,
        related_name="auction_bids"
    )
    # Timestamp
    timestamp = models.DateTimeField(auto_now_add=True)
    pass


# Done
class Comment(models.Model):
    # User (foreign)
    commenter = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name="user_comments"
    )
    # Auction (foreign)
    listing = models.ForeignKey(
        'Auction',
        on_delete=models.CASCADE,
        related_name="auction_comments"
    )
    # Comment
    content = models.TextField()
    # Timestamp
    timestamp = models.DateTimeField(auto_now_add=True)
    pass
