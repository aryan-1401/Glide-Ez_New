from django.shortcuts import HttpResponse, render
from django.http import HttpResponse
# Create your views here.

def home(request): 
    return render(request, "glideEz/index.html")

def destination_view(request):
    return render(request, "glideEz/destination.html")

def login_user_view(request):
    return render(request, "glideEz/login_user.html")

def login_airline_view(request):
    return render(request, "glideEz/login_airline.html")

def pricing_view(request):
    return render(request, "glideEz/pricing.html")
    