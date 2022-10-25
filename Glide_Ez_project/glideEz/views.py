from django.shortcuts import HttpResponse, render
from django.http import HttpResponse
from django.core.mail import send_mail
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

def contact_view(request):
    # TODO: fix no message in email
    if request.method == 'POST':
        name = request.POST.get('visitor_name')
        email = request.POST.get('visitor_email')
        subject = request.POST.get('email_title')
        message = request.POST.get('visitor_message')
        form_data = {
            'name':name,
            'email':email,
            'subject':subject,
            'message':message
        }
        message = '''
        From:\n\t\t{}\n
        Message:\n\t\t{}\n
        Email:\n\t\t{}\n
        Subject:\n\t\t{}\n
        '''.format(form_data['name'], form_data['message'], form_data['email'],form_data['subject'])
        send_mail('You got a mail!', message, '', ['glideezinfo@gmail.com']) # TODO: enter your email address
    return render(request, "glideEz/contact.html")
    