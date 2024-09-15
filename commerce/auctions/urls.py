from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path('create/', views.createListing, name='createListing'), #hvor skal man have / efter create?
    path("register", views.register, name="register"),
    path('adminpage/', admin.site.urls),
]
