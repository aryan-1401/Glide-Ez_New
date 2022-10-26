from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("destination", views.destination_view, name="destination"),
    path("login_user", views.login_user_view, name="login_user"),
    path("register_user", views.register_user_view, name="register_user"),
    path("login_airline", views.login_airline_view, name="login_airline"),
    path("logout", views.logout_view, name="logout"),
    path("pricing", views.pricing_view, name="pricing"),
    path("contact", views.contact_view, name="contact")
    
]