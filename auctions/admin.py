from django.contrib import admin
from auctions.models import *

# Register your models here.
admin.site.register(listing)
admin.site.register(Bid)

admin.site.register(comments)
admin.site.register(User)
