from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting",views.createlisting,name="createlisting"),
    path("listing/<int:listing_id>",views.list,name="list"),
    path("closelist/<int:listing_id>",views.closelist,name="closelist"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("listing/<int:listing_id>/subscribe",views.subscribe,name="subscribe"),
    path("listing/<int:listing_id>/unsubscribe",views.unsubscribe,name="unsubscribe"),
    path("categories",views.categories,name="categories"),
    path("categoreis/<str:category>",views.category,name="category"),
    path("listing/<int:listing_id>/bid",views.bids,name="bids"),
    path("closedlisting",views.closed_listing,name="closed_listing")
]
