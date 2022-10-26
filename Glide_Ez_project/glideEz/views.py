from django.shortcuts import HttpResponse, redirect, render
from django.http import HttpResponse
from django.core.mail import send_mail
# for stopping session on clicking back button
from django.views.decorators.cache import cache_control

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
            # Save email in session
            request.session['email'] = email
           
           # Capitalize first letter of user name
            first_name = user_name[0].capitalize()
            # Get address of user
            mycursor.execute("SELECT address FROM user WHERE Email = %s AND passwrd = %s", (email, password))
            address = mycursor.fetchone()
            # Get phone number of user
            mycursor.execute("SELECT phone_no FROM user WHERE Email = %s AND passwrd = %s", (email, password))
            phone_number = mycursor.fetchone()
            # Get aadhar number of user
            mycursor.execute("SELECT adhaar_no FROM user WHERE Email = %s AND passwrd = %s", (email, password))
            aadhar = mycursor.fetchone()
            # Get date of birth of user
            mycursor.execute("SELECT DOB FROM user WHERE Email = %s AND passwrd = %s", (email, password))
            dob = mycursor.fetchone()
            # create dict to store user details
            user = {
                'first_name': first_name,
                'email': email,
                'address': address[0],
                'phone_number': phone_number[0],
                'aadhar': aadhar[0],
                'dob': dob[0]

            }
        

            return render(request, "glideEz/index.html", {'user': user})
            # return render(request, "glideEz/index.html", user)
            # return render(request, "glideEz/index.html", {'user_name': first_name})
        else:
            return HttpResponse("User not found")
    return render(request, "glideEz/login_user.html")

def login_airline_view(request):
    return render(request, "glideEz/login_airline.html")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_view(request):
    # Delete user name from session
    del request.session['user_name']
    # stop session on clicking back button

    return render(request, "glideEz/index.html")

def view_account_view(request):
    # Get email from session
    email = request.session['email']
    
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="2002",
        database="glide_ez"
    )
    mycursor = mydb.cursor()
    # Fetch user first name from session
    user_name = request.session['user_name']
    # fetch user address from database
    mycursor.execute("SELECT address FROM user WHERE Email = %s", (email,))
    address = mycursor.fetchone()
    # fetch user phone number from database
    mycursor.execute("SELECT phone_no FROM user WHERE Email = %s", (email,))
    phone_number = mycursor.fetchone()
    # fetch user aadhar number from database
    mycursor.execute("SELECT adhaar_no FROM user WHERE Email = %s", (email,))
    aadhar = mycursor.fetchone()
    # fetch user date of birth from database
    mycursor.execute("SELECT DOB FROM user WHERE Email = %s", (email,))
    dob = mycursor.fetchone()
    # create dict to store user details
    user = {

        'first_name': user_name,
        'email': email,
        'address': address[0],
        'phone_number': phone_number[0],
        'aadhar': aadhar[0],
        'dob': dob[0]

    }
    return render(request, "glideEz/view_account.html", {'user': user})
   
     

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
    