from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
class listing(models.Model):
	status=models.BooleanField(default=True)
	title=models.CharField(max_length=65)
	description=models.CharField(max_length=300)
	category=models.CharField(max_length=64,blank=True)
	start_bid=models.FloatField()
	image=models.URLField()
	date=models.DateTimeField()
	creator=models.ForeignKey(User,on_delete=models.CASCADE,related_name="listings")
	subscribers=models.ManyToManyField(User,blank=True,related_name="watchlist")
	def __str__(self):
		return f"{self.title} id :{self.id} created on :{self.date}" 

class Bid(models.Model):
	value=models.IntegerField()
	date=models.DateTimeField()
	user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="bids")
	list=models.ForeignKey(listing,on_delete=models.CASCADE,related_name="bids")
	def __str__(self):
		return f"{self.value}"

class comments(models.Model):
	text=models.CharField(max_length=600)
	user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="comments")
	date=models.DateTimeField()
	lists=models.ForeignKey(listing,on_delete=models.CASCADE,related_name="comments")
	def __str__(self):
		return f"{self.user}:{self.text}"

