from django.shortcuts import HttpResponse, redirect, render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.views.decorators.cache import cache_control # for stopping session on clicking back button
import mysql.connector
from datetime import datetime
from django.contrib import messages #import messages
import sweetify

# Create your views here.
def home(request): 
    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2002",
            database="glide_ez"
        )
    mycursor = mydb.cursor()
    mycursor.execute('select distinct loc from Airport order by loc;')
    details=mycursor.fetchall()
    print(details)
    print('Hi')
    return render(request, "glideEz/index.html",{'details' : details})

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
            sweetify.error(request, 'Registration Failed', text='User Already exists', persistent='Try Again')
            return redirect('/register_user')
            # return redirect('register_user')
        else:
            mycursor.execute("select max(User_ID) from User;")
            id=mycursor.fetchall()
            name=name.split(' ')
            if(len(name)<3):
                name.append('')
            if(len(name)<3):
                name.append('')
            mycursor.execute("INSERT INTO user (User_ID, first_name, middle_name,LAst_Name ,Email, passwrd, adhaar_no, address, DOB, phone_no) VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)", (id[0][0]+1,name[0],name[1],name[2],email, password, aadhar, address, dob, phone_number))
            mydb.commit()
            sweetify.success(request, 'Registration Successfull', text='Your account was created successfully!', persistent='Login')
            return redirect('/login_user')
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
            request.session['user_name'] = user_name[0].capitalize()
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
        else:
            sweetify.error(request, 'User Not Found', text='User doesn\'t exist', persistent='Try Again')
            return redirect('/login_user')
    return render(request, "glideEz/login_user.html")

def register_airline_view(request):
    if request.method == "POST":
        # Getting airline name
        name = request.POST.get('name')
        # Getting airline email
        email = request.POST.get('email')
        # Getting airline password
        password = request.POST.get('pass')
        # Getting airline address
        address = request.POST.get('loc')
        # Getting airline phone number
        phone_number = request.POST.get('phone')

        #check if airline exists in mysql database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2002",
            database="glide_ez"
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM airline WHERE Email = %s", (email,))
        airline = mycursor.fetchone()
        if airline:
            sweetify.error(request, 'Registration Failed', text='Airline Already exists', persistent='Try Again')
            return redirect('/register_airline')
        else:

            # Generate unique airline id which is not present in database which starts with first two letters of airline name
            airline_id = name[0:2]
            mycursor.execute("SELECT airline_id FROM airline")
            airline_ids = mycursor.fetchall()
            for i in range(1, 100):
                if (airline_id + str(i),) not in airline_ids:
                    airline_id = airline_id + str(i)
                    break

            
            mycursor.execute("INSERT INTO airline (Airline_ID, Airline_name, passwrd, Email, phone_no, location) VALUES (%s, %s, %s, %s, %s, %s)", (airline_id, name, password, email, phone_number, address))
            mydb.commit()
            sweetify.success(request, 'Registration Successfull', text='Your account was created successfully!', persistent='Login')
            return redirect('/login_airline')
    return render(request, "glideEz/login_airline.html")
    

def login_airline_view(request):
    if request.method == "POST":
        # Getting airline email
        email = request.POST.get('login_email')
        # Getting airline password
        password = request.POST.get('login_password')

        #check if airline exists in mysql database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2002",
            database="glide_ez"
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM airline WHERE Email = %s AND passwrd = %s", (email, password))
        airline = mycursor.fetchone()
        if airline:
            # Fetch airline name from database
            mycursor.execute("SELECT Airline_name FROM airline WHERE Email = %s AND passwrd = %s", (email, password))
            airline_name = mycursor.fetchone()

            # Save airline name in session
            request.session['airline_username'] = airline_name[0].capitalize()
            # Save email in session
            request.session['email'] = email
            # Capitalize first letter of airline name
            first_name = airline_name[0].capitalize()
            # Get address of airline
            mycursor.execute("SELECT location FROM airline WHERE Email = %s AND passwrd = %s", (email, password))
            address = mycursor.fetchone()
            # Get phone number of airline
            mycursor.execute("SELECT phone_no FROM airline WHERE Email = %s AND passwrd = %s", (email, password))
            phone_number = mycursor.fetchone()
            # Get airline id of airline
            mycursor.execute("SELECT Airline_ID FROM airline WHERE Email = %s AND passwrd = %s", (email, password))
            airline_id = mycursor.fetchone()
            # create dict to store airline details
            airline = {
                'first_name': first_name,
                'email': email,
                'address': address[0],
                'phone_number': phone_number[0],
                'airline_id': airline_id[0]

            }
            print(airline)
            return render(request, "glideEz/Airline_Home.html", {'airline': airline})
        else:
            sweetify.error(request, 'Airline Not Found', text='Airline doesn\'t exist', persistent='Try Again')
            return redirect('/login_airline')
    return render(request, "glideEz/login_airline.html")


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_view(request):
    # if user is logged in
    if request.session.has_key('user_name'):
        # delete user_name and email from session
        del request.session['user_name']
        del request.session['email']
        # redirect to home page
        return redirect('/')
    # if airline is logged in
    elif request.session.has_key('airline_name'):
        # delete airline_name and email from session
        del request.session['airline_name']
        del request.session['email']
        # redirect to home page
        return redirect('/')

    return redirect('/')

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

def bookings_view(request):
    # Get email from session
    print(request.session['email'])
    return render(request, "glideEz/bookings.html")

def contact_view(request):
    # TODO: fix no message in email
    if request.method == 'POST':
        name = request.POST.get('visitor_name')
        email = request.POST.get('visitor_email')
        new_message = request.POST.get('visitor_message')
        subject = request.POST.get('email_title')
        form_data = {
            'name':name,
            'email':email,
            'subject':subject,
            'new_message':new_message
        }
        message = '''
        From:\n\t\t{}\n
        Message:\n\t\t{}\n
        Email:\n\t\t{}\n
        Subject:\n\t\t{}\n
        '''.format(form_data['name'], form_data['new_message'], form_data['email'],form_data['subject'])
        send_mail('You got a mail!', message, '', ['glideezinfo@gmail.com']) # TODO: enter your email address
    return render(request, "glideEz/contact.html")
    
def search_flight_view(request):
    if request.method == "POST":
        # Get user input
        source = request.POST.get('source')
        print(source)
        destination = request.POST.get('destination')
        print(destination)
        class_type = request.POST.get('class')      
        date = request.POST.get('date_travel')
        print((date))
        
        print(class_type)
        #Convert date MM/DD/YYYY to YYYY-MM-DD
        date = datetime.strptime(date, '%m/%d/%Y').strftime('%Y-%m-%d')

        # Connect to database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2002",
            database="glide_ez"
        )
        mycursor = mydb.cursor()

        # str = """with tempsrc(tempID) as 
        # (SELECT Airport_ID from Airport where loc LIKE '%{}%') , 
        # tempdest(tempID) as (SELECT Airport_ID from Airport where loc LIKE '%{}%') 
        # select Depart_time,Arrival_time from trip,tempsrc,tempdest where trip.src_ID = tempsrc.tempID and
        #  trip.dest_ID = tempdest.tempID AND trip.depart_time LIKE '%{}%'; """.format(source,destination,date)
        
        str = """with temp1(src,dest) as (select s.Airport_ID,t.Airport_ID from Airport s,Airport t 
        where s.loc='{}' and t.loc='{}') , temp2(tr_ID,arr,dept,FL_ID) as 
        (select Trip.Trip_ID,Trip.Arrival_Time,Trip.Depart_Time,Flight_ID from Trip,temp1 
        where Trip.Depart_Time LIKE '{}%' and Trip.src_ID=temp1.src and Trip.dest_ID=temp1.dest) 
        Select Flight.Flight_ID,Airline.Airline_Name,temp2.dept,temp2.arr,Seat.Price from Airline,Flight,temp2,Seat 
        where Airline.Airline_Id=Flight.fk_Airline_ID and Flight.Flight_ID=temp2.FL_ID and 
        Seat.Trip_ID=temp2.tr_ID and Seat.Class_type='{}'
         ;""".format(source,destination,date,class_type)
        mycursor.execute(str)
        details = mycursor.fetchall()
        print(details)
    

        # Extract time from datetime in details[0]
        # depart_time = details[0][0].time()
        # arrival_time = details[0][1].time()

        # details_dict= {

        #     'source':source,
        #     'destination':destination,
        #     'class_type':class_type,
        #     'date':date,
        #     'airline_name':details[0][2],

        #     'depart_time':depart_time,
        #     'arrival_time':arrival_time
        # }
        print(details)
        return render(request, "glideEz/search_flight.html", {'details': details , 'source' : source , 'destination' : destination , 'Class_Type' : class_type})



def airline_home_view(request):
    return render(request,'glideEz/Airline_Home.html')

def airline_addtrip_view(request):
    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2002",
            database="glide_ez"
        )
    mycursor = mydb.cursor()
    mycursor.execute('select distinct loc from Airport order by loc;')
    details=mycursor.fetchall()
    print(details)
    print('Hi')
    return render(request,'glideEz/airline_addtrip.html',{'details' : details})

def airline_pricing_view(request):
    return render(request,'glideEz/airline_pricing.html')

def airline_contact_view(request):
    return render(request,'glideEz/airline_contact.html')

def airline_flight_view(request):
    return render(request,'glideEz/addflight.html')


       