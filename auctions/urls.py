from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="create"),
    path("comment", views.addComment, name="comment"),
    path("bid", views.placeBid, name="bid"),
    path("close", views.closeAuction, name="close"),
    path("addToWatchList", views.addToWatchList, name="add"),
    path("removeFromWatchList", views.removeFromWatchList, name="remove"),
    path("watchList", views.renderWatchList, name="watch"),
    path("categories", views.renderCategories, name="category"),
    path("listing/<str:category>", views.categoryListing, name="catList"),
    path("<str:id>", views.renderListing, name="listing"),
]
