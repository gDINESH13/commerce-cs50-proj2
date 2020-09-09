from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .models import *


def index(request):
    listings=listing.objects.all()
    l=[]
    for i in listings:
        if len(i.description)>130:
            i.description=i.description[0:128]+"...."
    for i in listings:
        if i.status :
            l.append(i)
    return render(request, "auctions/index.html",{"listings":l,"status":True})


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
def createlisting(request):
    if request.method=="POST":
        user=request.user
        title=request.POST["title"]
        description=request.POST["description"]
        category=request.POST["category"]
        bid=request.POST["place_bid"]
        image=request.POST["url"]
        date=datetime.datetime.now()
        list=listing(title=title,description=description,category=category,start_bid=bid,image=image,date=date,creator=user)
        list.save()
        return HttpResponseRedirect(reverse("index"))
    if request.method=="GET":
        return render(request,"auctions/create_listing.html")


def list(request,listing_id):
    l=listing.objects.get(id=listing_id)
    if request.user.is_authenticated:
        iswatchlist=request.user.watchlist.filter(id=listing_id).exists()
        if request.method=="POST":
            user=request.user
            date=datetime.datetime.now()
            te=request.POST.get('text')
            comment=comments(date=date,user=user,text=te,lists=l)
            comment.save()
         

        return render(request,"auctions/listings.html",
                {"list":l,"watchlist":iswatchlist,"bids":l.bids,"comments":l.comments.all(),"one":1 })
    elif request.method=="GET":
        return render(request,"auctions/listings.html",{"list":l,"bids":l.bids
            })
@login_required
def subscribe(request,listing_id):
    if request.method=="POST":
        list=listing.objects.get(id=listing_id)
        user=request.user
        list.subscribers.add(user)
        list.save()
    return HttpResponseRedirect(reverse('list' ,args=[listing_id,])) 
@login_required
def unsubscribe(request,listing_id):
    if request.method=="POST":
        list=listing.objects.get(id=listing_id)
        user=request.user
        list.subscribers.remove(user)
        list.save()
    return HttpResponseRedirect(reverse('list',args=[listing_id,]))
#@login_required
def closelist(request,listing_id):
    if request.method=="POST":
        list=listing.objects.get(pk=listing_id)
        list.status=False
        list.save()
    return HttpResponseRedirect(reverse('index'))
@login_required
def watchlist(request):
    if request.user.is_authenticated:
        watchlist=request.user.watchlist.all()
        return render(request,"auctions/watchlist.html",{'watchlist':watchlist})
    return HttpResponseRedirect(reverse("index"))
@login_required
def categories(request):
    list=listing.objects.all()
    categories=set()
    '''for i in list:
        if i.category != "":
            categories.add(i.category)'''
    for i in list:
        if i.status:
            categories.add(i.category)
    return render(request,"auctions/categories.html",{"categories":categories})

def category(request,category):
    listings=listing.objects.filter(category=category)
    for i in listings:
        if len(i.description)>130:
            i.description=i.description[0:128]+"...."
    return render(request,"auctions/category.html",{"listings":listings})
def bids(request,listing_id):
    if request.method=="POST":
        list=listing.objects.get(pk=listing_id)
        value=int(request.POST["bid"])
        user=request.user
        date=datetime.datetime.now()
        last_bid=list.bids.last()
        bid=Bid(value=value,user=user,list=list,date=date)
        flag=0
        if last_bid is not None:
            if value>last_bid.value:
                bid.save()
                flag=1
        elif value>list.start_bid:
            bid.save()
            flag=1
        if flag==0:
            messages.error(request,"Your bid is not greater than the current bid.")

    return HttpResponseRedirect(reverse('list',args=[listing_id,]))
   
def closed_listing(request):
    list=listing.objects.all()
    l=[]
    
    for i in list:
        if i.status == False:
            l.append(i)

    return render(request,"auctions/index.html",{"listings":l,"status":False})





