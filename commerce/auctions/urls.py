from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path('create', views.createListing, name='createListing'), 
    path("register", views.register, name="register"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("like/<int:object_id>", views.like, name="like"),
    path("test", views.test_view, name="test"),
    path("error", views.error_view, name="error"),
]
