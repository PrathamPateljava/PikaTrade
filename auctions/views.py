from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import User,Category,Listing,Comment,Bid


def index(request):
    activeListing=Listing.objects.filter(isActive=True)
    categories=Category.objects.all()
    return render(request, "auctions/index.html",{
        "listings":activeListing,
        "categories":categories
    })

def createListing(request):
    if request.method=='POST':
        title=request.POST['title']
        desc=request.POST['description']
        imageurl=request.POST['imageurl']
        price=request.POST['price']
        category=request.POST['category']
        categoryData=Category.objects.get(name=category)
        currentUser=request.user

        bid=Bid(bid=price,user=currentUser)
        bid.save()

        newListing=Listing(title=title,desc=desc,imageurl=imageurl,price=bid,category=categoryData,owner=currentUser)
        newListing.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        categories=Category.objects.all()
        return render(request,"auctions/create.html",{
            "categories":categories
        })

def filterCategory(request):
    if request.method=='POST':
        selCategory=request.POST['category']
        print(selCategory)
        cat=Category.objects.get(name=selCategory)
        filteredListing=Listing.objects.filter(isActive=True,category=cat)
        categories=Category.objects.all()
        return render(request,"auctions/index.html",{
            "listings":filteredListing,
            "categories":categories
        })
    else:
        activeListing=Listing.objects.filter(isActive=True)
        categories=Category.objects.all()
        return render(request, "auctions/index.html",{
            "listings":activeListing,
            "categories":categories
    })

def listing(request,id):
    listing=Listing.objects.get(pk=id)
    iswatching=request.user in listing.watchlist.all()
    comments=Comment.objects.filter(listing=listing)
    isOwner= request.user.username==listing.owner.username
    return render(request,"auctions/listing.html",{
        "listing":listing,
        "iswatching":iswatching,
        "comments":comments,
        "isOwner":isOwner,
    })

def remove(request,id):
    listing=Listing.objects.get(pk=id)
    curruser=request.user
    listing.watchlist.remove(curruser)
    return HttpResponseRedirect(reverse("listing",args=(id, )))

def add(request,id):
    listing=Listing.objects.get(pk=id)
    curruser=request.user
    listing.watchlist.add(curruser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def watchlist(request):
    curruser=request.user
    categories=Category.objects.all()
    listings=curruser.watching.all()
    return render(request,"auctions/watchlist.html",{
        "listings":listings,
        "categories":categories
    })

def addComment(request,id):
    curruser=request.user
    listing=Listing.objects.get(pk=id)
    message=request.POST['newComment']

    comment=Comment(author=curruser,listing=listing,message=message)

    comment.save()
    return HttpResponseRedirect(reverse('listing',args=(id, )))

def addBid(request,id):
    newBid=request.POST['bidAmount']
    listing=Listing.objects.get(pk=id)
    if float(newBid) > listing.price.bid:
        updatedBid=Bid(user=request.user,bid=float(newBid))
        updatedBid.save()
        print(updatedBid)
        listing.price=updatedBid
        listing.save()
        print(listing.price)
        messages.success(request,"Bid Updated Succesfully")
        return HttpResponseRedirect(reverse("listing",args=(id,)))
    else:
        messages.error(request,"Bid Updated Succesfully")
        return HttpResponseRedirect(reverse("listing",args=(id, )))
        # return render(request,"auctions/listing.html",{
        #     "message":"Bid was not updated",
        #     "listing":listing,
        #     "updated":False,
        #     "comments":comments,
        #     "isOwner":isOwner
        # })

def close(request,id):
    listing=Listing.objects.get(pk=id)
    listing.isActive=False
    listing.save()
    comments=Comment.objects.filter(listing=listing)
    isOwner= request.user.username==listing.owner.username
    return render(request,"auctions/listing.html",{
            "message":"Your Bid was closed successfully",
            "listing":listing,
            "updated":False,
            "comments":comments,
            "isOwner":isOwner
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

def closedListings(request):
    closedListing=Listing.objects.filter(isActive=False)
    categories=Category.objects.all()
    return render(request, "auctions/index.html",{
        "listings":closedListing,
        "categories":categories
    })


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
