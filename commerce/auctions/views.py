from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid

def closeAuction(request, id):
    list = Listing.objects.get(pk=id)
    list.is_active = False
    list.save()
    return HttpResponseRedirect(reverse(index))

def listing(request, id):
    list = Listing.objects.get(pk=id)
    islistin = request.user in list.watchlist.all()
    all_comments = Comment.objects.filter(listing=list)
    isowner = request.user.username == list.owner.username
    return render(request, "auctions/listing.html", {
        "listing": list,
        "is_list_in": islistin, 
        "comments": all_comments,
        "isowner": isowner
    })

def addComment(request, id):
    current_user = request.user 
    list_data = Listing.objects.get(pk=id)
    message = request.POST["newcomment"]

    new_comment = Comment(
        author = current_user, 
        listing = list_data,
        message = message
    )
    new_comment.save()

    return HttpResponseRedirect(reverse(listing, args=(id, )))

def removeFromWatchlist(request, id):
    list_data = Listing.objects.get(pk=id)
    current_user = request.user
    list_data.watchlist.remove(current_user)
    return HttpResponseRedirect(reverse(listing, args=(id, )))

def displayWatchlist(request):
    current_user = request.user
    listings = current_user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "Listings": listings
    })

def addToWatchlist(request, id):
    list_data = Listing.objects.get(pk=id)
    current_user = request.user
    list_data.watchlist.add(current_user)
    return HttpResponseRedirect(reverse(listing, args=(id, )))

def index(request):
    act_list = Listing.objects.filter()
    all_cat = Category.objects.all()

    return render(request, "auctions/index.html", {
        "Listings": act_list,
        "categories": all_cat
    })

def displayCategory(request):
    if request.method == "POST":
        ch_category = request.POST["category"]
        kategorija = Category.objects.get(category_name=ch_category)
        act_list = Listing.objects.filter(is_active=True, category=kategorija)
        all_cat = Category.objects.all()

        return render(request, "auctions/index.html", {
            "Listings": act_list,
            "categories": all_cat
        })


def addBid(request, id):
    newbid = request.POST["addbid"]
    list = Listing.objects.get(pk=id)
    if float(newbid) > list.price.bid:
        Updatebid = Bid(user = request.user, bid=float(newbid))
        Updatebid.save()
        list.price = Updatebid
        list.save()
    return HttpResponseRedirect(reverse(listing, args=(id, )))

def createListing(request):
    if request.method == "GET":
        all_cat = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": all_cat
        })
    else:
        title = request.POST["title"]
        desc = request.POST["desc"]
        img_url = request.POST["imgurl"]
        price = request.POST["price"]
        category = request.POST["category"]
        category_data = Category.objects.get(category_name=category)
        current_user = request.user

        _bid = Bid(bid=float(price), user=current_user)
        _bid.save()

        newListing = Listing(
            title = title,
            description = desc,
            imgUrl = img_url,
            price = _bid,
            category = category_data,
            owner = current_user
        )

        newListing.save()
        
        return HttpResponseRedirect(reverse(index))

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
