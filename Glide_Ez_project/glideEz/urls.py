from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("destination", views.destination_view, name="destination"),
    path("login_user", views.login_user_view, name="login_user"),
    path("login_airline", views.login_airline_view, name="login_airline"),
    path("pricing", views.pricing_view, name="pricing"),
    path("contact", views.contact_view, name="contact")
    
]