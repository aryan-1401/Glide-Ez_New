from django.shortcuts import HttpResponse, render
from django.http import HttpResponse
# Create your views here.

def home(request): 
    return render(request, "glideEz/index.html")

    