from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("destination", views.destination_view, name="destination"),
    path("login_user", views.login_user_view, name="login_user"),
    path("register_user", views.register_user_view, name="register_user"),
    path("register_airline", views.register_airline_view, name="register_airline"),
    path("login_airline", views.login_airline_view, name="login_airline"),
    path("logout", views.logout_view, name="logout"),
    path("view_account", views.view_account_view, name="view_account"),
    path("pricing", views.pricing_view, name="pricing"),
    path("contact", views.contact_view, name="contact"),
    path("bookings", views.bookings_view, name="bookings"),
    path("search_flight", views.search_flight_view, name="search_flight"),
    path("book_flight", views.book_flight_view, name="book_flight"),
    path("payment", views.payment_view, name="payment"),
    path("airline_home", views.airline_home_view, name="airline_home"),
    path("airline_contact", views.airline_contact_view, name="airline_contact"),
    path("airline_pricing", views.airline_pricing_view, name="airline_pricing"),
    path("airline_addTrip", views.airline_addtrip_view, name="airline_addTrip"),
    path("airline_addflight", views.airline_flight_view, name="airline_addflight"),
    path("forgot_password", views.forgot_password_view, name="forgot_password"),
    path("addflight", views.addflight_view, name="addflight"),
    path("addtrip", views.addtrip_view, name="addtrip")
]