from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.createListing,name="create"),
    path("category",views.filterCategory,name="category"),
    path("listing/<int:id>",views.listing,name="listing"),
    path("remove/<int:id>",views.remove,name="remove"),
    path("add/<int:id>",views.add,name="add"),
    path("watchlist",views.watchlist,name="watchlist"),
    path("addComment/<int:id>",views.addComment,name="addComment"),
    path("addBid/<int:id>",views.addBid,name="bid"),
    path("close/<int:id>",views.close,name="close"),
    path("closedListings",views.closedListings,name="closedListing")
]
