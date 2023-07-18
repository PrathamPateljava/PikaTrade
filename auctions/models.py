from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name=models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Bid(models.Model):
    bid=models.FloatField(default=0)
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,related_name="userBid")

    def __str__(self):
        return f" {self.user} bid {str(self.bid)}"

class Listing(models.Model):
    title=models.CharField(max_length=64)
    desc=models.CharField(max_length=100)
    imageurl=models.CharField(max_length=200)
    price=models.ForeignKey(Bid,on_delete=models.CASCADE,blank=True,null=True,related_name="bidPrice")
    isActive=models.BooleanField(default=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,related_name="user")
    category=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,related_name="category")
    watchlist=models.ManyToManyField(User,blank=True,null=True,related_name="watching")

    def __str__(self):
        return f"{self.title} : {self.price}"

class Comment(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="userComment")
    listing=models.ForeignKey(Listing,on_delete=models.CASCADE,blank=True,null=True,related_name="commentProduct")
    message=models.CharField(max_length=200)

    def __str__(self):
        return f"{self.author} commented on {self.listing}"
