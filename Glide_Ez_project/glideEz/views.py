from django.shortcuts import HttpResponse, redirect, render
from django.http import HttpResponse
from django.core.mail import send_mail

#mysql connector
import mysql.connector
# Create your views here.

def home(request): 
    return render(request, "glideEz/index.html")

def destination_view(request):
    return render(request, "glideEz/destination.html")

def register_user_view(request):
    if request.method == "POST":
        # Getting user name
        name = request.POST.get('username')
        # Getting user email
        email = request.POST.get('email')
        # Getting user password
        password = request.POST.get('pass')
        #Getting user date of birth
        dob = request.POST.get('dob')
        # Getting user address
        address = request.POST.get('address')
        #Getting user aadhar number
        aadhar = request.POST.get('aadhar')
        # Getting user phone number
        phone_number = request.POST.get('phone')
        

        #check if user exists in mysql database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2002",
            database="glide_ez"
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM user WHERE Email = %s", (email,))
        user = mycursor.fetchone()
        if user:
            return HttpResponse("User already exists")
        else:
            mycursor.execute("INSERT INTO user (first_name, Email, passwrd, adhaar_no, address, DOB, phone_no) VALUES (%s, %s, %s, %s, %s, %s, %s)", (name, email, password, aadhar, address, dob, phone_number))
            mydb.commit()
            return render(request, "glideEz/login_user.html")
    return render(request, "glideEz/login_user.html")

def login_user_view(request):
    if request.method == "POST":
        # Getting user email
        email = request.POST.get('login_email')
        # Getting user password
        password = request.POST.get('login_password')

        #check if user exists in mysql database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2002",
            database="glide_ez"
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM user WHERE Email = %s AND passwrd = %s", (email, password))
        user = mycursor.fetchone()
        if user:
            # Fetch user first name from database
            mycursor.execute("SELECT first_name FROM user WHERE Email = %s AND passwrd = %s", (email, password))
            user_name = mycursor.fetchone()

            # Save username in session
            request.session['user_name'] = user_name[0]
            # return HttpResponse("Welcome "+ user_name[0])
            #Display user name on home page
            return render(request, "glideEz/index.html", {'user_name': user_name[0]})
            # return render(request, "glideEz/index.html")
        else:
            return HttpResponse("User not found")
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
        message = request.POST.get('visitor_message')
        subject = request.POST.get('email_title')
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
    