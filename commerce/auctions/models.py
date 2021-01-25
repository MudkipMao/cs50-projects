from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Watchlist (M2M)
    watched_listings = models.ManyToManyField(
        'Auction',
        related_name="user_watchlist",
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
    # Watchlist
    # Title
    title = models.CharField(max_length=64)
    # Description
    description = models.CharField(max_length=64)
    # Starting price
    # URL for image (optional)
    image = models.ImageField(blank=True, )
    # Category (foreign)(optional)
    # Bids
    # Timestamp
    pass


class Bid(models.Model):
    # User (foreign)
    # Price
    # Auction (foreign)
    # Timestamp
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


class Winner(models.Model):
    # User (foreign)
    # Auction (foreign)
    # Win price (foreign)
    # Win time
    pass
