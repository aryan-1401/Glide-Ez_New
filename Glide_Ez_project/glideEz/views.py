from gettext import npgettext
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
    return render(request, "glideEz/index.html",{'details' : details})


def destination_view(request):
    return render(request, "glideEz/destination.html")


def pricing_view(request):
    return render(request, "glideEz/pricing.html")


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
        mycursor.execute("SELECT * FROM user WHERE Email = '{}'".format(email))
        user = mycursor.fetchone()
        if user:
            sweetify.error(request, 'Registration Failed', text='User Already exists', persistent='Try Again')
            return redirect('/register_user')
            # return redirect('register_user')
        else:
            # TODO: fix format of query
            mycursor.execute("""INSERT INTO user (User_ID, first_name ,Middle_Name,Last_name, Email , passwrd, adhaar_no, address, DOB, phone_no) VALUES (null,'{}',null,null,'{}','{}',{},'{}','{}',{});
            """.format(name, email , password, aadhar, address, dob, phone_number))
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
            return redirect('/', {'user': user})
        #else if email is in database but password is wrong
        elif user is None:
            mycursor.execute("SELECT * FROM user WHERE Email = %s", (email,))
            user = mycursor.fetchone()
            if user:
                sweetify.error(request, 'Login Failed', text='Wrong Password', persistent='Try Again')
                return redirect('/login_user')
            else:
                sweetify.error(request, 'Login Failed', text='Email not Found', persistent='Try Again')
                return redirect('/login_user')
    return render(request, "glideEz/login_user.html")


def forgot_password_view(request):
    # send email to user with link to reset password with smtp
    if request.method == 'POST':
        email = request.POST.get('email')
        # send user his old password via email
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2002",
            database="glide_ez"
        )
        mycursor = mydb.cursor()
        mycursor.execute("select passwrd from User where Email = '{}'".format(email))
        details = mycursor.fetchall()
        # print(details)
        if details:
            send_mail('Your password', details[0][0], '', [email])
            sweetify.info(request, 'Password Sent Successfully.', button='Ok', timer=3000)
            return render(request, 'glideEz/forgot_password.html')
        else:
            sweetify.error(request, 'Email Not Found', text='Email doesn\'t exist', persistent='Try Again')
            return render(request, 'glideEz/forgot_password.html', {'message': 'Email not found'})
    return render(request, 'glideEz/forgot_password.html')


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
    #convert phone number to string
    phone_number = str(phone_number[0])
    # fetch user aadhar number from database
    mycursor.execute("SELECT adhaar_no FROM user WHERE Email = %s", (email,))
    aadhar = mycursor.fetchone()
    #convert aadhar number to string
    aadhar = str(aadhar[0])
    # fetch user date of birth from database
    mycursor.execute("SELECT DOB FROM user WHERE Email = %s", (email,))
    dob = mycursor.fetchone()
    # convert date of birth to date format
    dob = dob[0].strftime("%d/%m/%Y")
    # create dict to store user details
    user = {

        'first_name': user_name,
        'email': email,
        'address': address[0],
        'phone_number': phone_number,
        'aadhar': aadhar,
        'dob': dob
    }
    print(user)
    return render(request, "glideEz/view_account.html", {'user': user})


# FIXME: BROKEN  
def edit_account_details_view(request):
    if request.method == "POST":
        #Get first name from form
        first_name = request.POST.get('first_name')
        print(first_name)
        #Get last name from form
        last_name = request.POST.get('last_name')
        print(last_name)
        #Get phone number from form
        phone_number = request.POST.get('phone_number')
        print(phone_number)
        #Get address from form
        address = request.POST.get('address')
        print(address)

        # Connect to mysql database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2002",
            database="glide_ez"
        )
        mycursor = mydb.cursor()
        # Get email from session
        email = request.session['email']
        print(email)
        # Update user details in database
        mycursor.execute("UPDATE user SET First_name = %s, Last_name = %s, phone_No = %s, Address = %s WHERE Email = %s", (first_name, last_name, phone_number, address, email))
        mydb.commit()
        
        # Save first name in session
        request.session['user_name'] = first_name
        # redirect to view account page
        return redirect('/view_account')
    else:
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
        #convert phone number to string
        phone_number = str(phone_number[0])
        # fetch user aadhar number from database
        mycursor.execute("SELECT adhaar_no FROM user WHERE Email = %s", (email,))
        aadhar = mycursor.fetchone()
        #convert aadhar number to string
        aadhar = str(aadhar[0])
        # fetch user date of birth from database
        mycursor.execute("SELECT DOB FROM user WHERE Email = %s", (email,))
        dob = mycursor.fetchone()
        # convert date of birth to date format
        dob = dob[0].strftime("%d/%m/%Y")
        # create dict to store user details
        user = {

            'first_name': user_name,
            'email': email,
            'address': address[0],
            'phone_number': phone_number,
            'aadhar': aadhar,
            'dob': dob
        }
        print(user)
        
        return render(request, "glideEz/edit_account_details.html", {'user': user})


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
        Select Flight.Flight_ID,Airline.Airline_Name,temp2.dept,temp2.arr,Seat.Price,tr_ID from Airline,Flight,temp2,Seat 
        where Airline.Airline_Id=Flight.fk_Airline_ID and Flight.Flight_ID=temp2.FL_ID and 
        Seat.Trip_ID=temp2.tr_ID and Seat.Class_type='{}' group by(tr_ID)
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


def book_flight_view(request):
    airline_name = request.GET.get('airline')
    flight_id = request.GET.get('flight_id')
    source = request.GET.get('source')
    destination = request.GET.get('destination')
    class_type = request.GET.get('Class_Type')
    departure_time = request.GET.get('departure_time')
    arrival_time = request.GET.get('arrival_time')
    price = request.GET.get('price')
    tr_ID = request.GET.get('tr_ID')

    if not request.session.has_key('email'):
        return redirect('/login_user')
    # connect to database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="2002",
        database="glide_ez"
    )
    mycursor = mydb.cursor()
    # Get all no of seats from flight table
    str = """select First_Class ,Business,Economy from Flight where Flight_ID = {};""".format(flight_id)
    mycursor.execute(str)
    seats = mycursor.fetchall()
    
    str="""select Seat_No,busy from Seat where Trip_ID={}""".format(tr_ID)
    mycursor.execute(str)
    seatno = mycursor.fetchall()

    economy_seats = int(seats[0][2])
    business_seats = int(seats[0][1])
    first_seats = int(seats[0][0])

    # Calculate no of rows for first class
    first_rows = first_seats//6
    
    

    # Calculate no of rows for business class
    business_rows = business_seats//6

    # Calculate no of rows for economy class
    economy_rows = economy_seats//6

    # Store all the details in a dictionary name book_details

    book_details = {
        'airline_name': airline_name,
        'flight_id': flight_id,
        'source': source,
        'destination': destination,
        'class_type': class_type,
        'departure_time': departure_time,
        'arrival_time': arrival_time,
        'price': price,
        'economy_seats': economy_seats,
        'business_seats': business_seats,
        'first_seats': first_seats,
        'first_rows': range(1,first_rows+1),
        'business_rows': range(1,business_rows+1),
        'economy_rows': range(1,economy_rows+1),
        'Seat_No' : seatno
    }
    return render(request, "glideEz/book_flight.html", {'book_details': book_details})


def payment_view(request):
    seat_list = request.POST.getlist('seats_selected')
    print("hellooooo")
    print(seat_list)
    # Get all the details from the form
    flight_id = request.POST.get('flight_id')
    print(flight_id)

    # if request.method == 'POST':
    #     # connect to database
    #     mydb = mysql.connector.connect(
    #         host="localhost",
    #         user="root",
    #         password="2002",
    #         database="glide_ez"
    #     )
    #     mycursor = mydb.cursor()
    #     # parse the seat list
    #     seat_list = request.POST.getlist('seats_selected')
    #     # check if seats are available or not in seat table
    #     for seat in seat_list:
    #         seat = seat.split('_')
    #         # check if seat is available or not
    #         str = """select * from Seat where fk_Flight_ID = {} and Seat_Row = {} and Seat_Number = {} and Seat_Status = 'Available';""".format(
    #             seat[0], seat[1], seat[2])
    #         mycursor.execute(str)
    #         details = mycursor.fetchall()
    #         if not details:
    #             sweetify.error(request, 'Seat Not Available', text='Seat is not available', persistent='Try Again')
    #             return redirect('/book_flight')
    #     # if seats are available then book the seats
    #     for seat in seat_list:
    #         seat = seat.split('_')
    #         # update seat status to booked
    #         str = """update Seat set Seat_Status = 'Booked' where fk_Flight_ID = {} and Seat_Row = {} and Seat_Number = {} and Seat_Status = 'Available';""".format(
    #             seat[0], seat[1], seat[2])
    #         mycursor.execute(str)
    #         mydb.commit()
    #         # insert into booking table
    #         str = """insert into Booking(fk_User_ID,fk_Flight_ID,Seat_Row,Seat_Number) values({}, {}, {}, {});""".format(
    #             request.session['user_id'], seat[0], seat[1], seat[2])
    #         mycursor.execute(str)
    #         mydb.commit()
    #     sweetify.success(request, 'Booking Successful', text='Booking Successful', persistent='Ok')
    #     return redirect('/book_flight')

    return render(request, 'glideEz/payment.html')


def bookings_view(request):
    return render(request, "glideEz/bookings.html")


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
            # Store airline id in session
            request.session['airline_id'] = airline_id[0]

            # create dict to store airline details
            airline = {
                'first_name': first_name,
                'email': email,
                'address': address[0],
                'phone_number': phone_number[0],
                'airline_id': airline_id[0]

            }
            # print(airline)
            # return redirect('airline_pricing', {'airline': airline})
            return render(request, "glideEz/Airline_Home.html", {'airline': airline})
        #else if email is in database but password is wrong
        elif airline is None:
            mycursor.execute("SELECT * FROM airline WHERE Email = %s", (email,))
            airline = mycursor.fetchone()
            if airline:
                sweetify.error(request, 'Login Failed', text='Wrong Password', persistent='Try Again')
                return redirect('/login_airline')
            else:
                sweetify.error(request, 'Login Failed', text='Email not Found', persistent='Try Again')
                return redirect('/login_airline')
    return render(request, "glideEz/login_airline.html")


def airline_home_view(request):
    return render(request,'glideEz/Airline_Home.html')


def airline_addflight_view(request):
    if request.method == "POST":
        Flight_ID = request.POST.get('Flight_ID')
        Flight_Name = request.POST.get('Flight_Name')
        First = request.POST.get('First')
        Business = request.POST.get('Business')
        Economy = request.POST.get('Economy')
        # Get airline id from session
        airline_id = request.session['airline_id']
        print(airline_id)
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2002",
            database="glide_ez"
        )
        mycursor = mydb.cursor()
        # Check if flight id already exists
        mycursor.execute("SELECT * FROM flight WHERE Flight_ID = %s", (Flight_ID,))
        flight = mycursor.fetchone()
        if flight:
            sweetify.error(request, 'Flight ID already exists', text='Try another flight id', persistent='Try Again')
            return redirect('/airline_addFlight')
        else:
            str="""insert into Flight(Flight_ID,fk_Airline_ID,Flight_Name,First_Class,Business_Class,Economy_Class) values({},'{}','{}',{},{},{})""".format(Flight_ID,airline_id,Flight_Name,First,Business,Economy)
            mycursor.execute(str)
            mydb.commit()
            sweetify.success(request, 'Flight Added', text='Flight Added Successfully', persistent='Add Trip')
            return redirect('/airline_addTrip')
    return render(request,'glideEz/addflight.html')


def airline_addtrip_view(request):
# mydb = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="2002",
#             database="glide_ez"
#         )
#     mycursor = mydb.cursor()
#     mycursor.execute('select distinct loc from Airport order by loc;')
#     details=mycursor.fetchall()
#     mycursor = mydb.cursor()
#     mycursor.execute('select Airport_Id,Airport_Name,loc from Airport order by loc;')
#     allairports=mycursor.fetchall()
#     return render(request,'glideEz/airline_addtrip.html',{'details' : details , 'airports' : allairports})
    Flight_ID = request.POST.get('Flight_ID')
    First_Class_Price = request.POST.get('First_Price')
    Business_Class_Price = request.POST.get('Business_Price')
    Economy_Class_Price = request.POST.get('Economy_Price')
    Source = request.POST.get('source')
    Source_airport = request.POST.get('source_ap')
    Destination = request.POST.get('destination')
    Destination_airport = request.POST.get('destination_ap')
    Departure = request.POST.get('departure')
    Arrival = request.POST.get('arrival')

    print(Flight_ID)
    print(First_Class_Price)
    print(Business_Class_Price)
    print(Economy_Class_Price)
    print(Source)
    print(Source_airport)
    print(Destination)
    print(Destination_airport)
    print(Departure)
    print(Arrival)

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="2002",
        database="glide_ez"
    )
    mycursor = mydb.cursor()
    # Get source airport id from airport table
    mycursor.execute("SELECT Airport_ID FROM airport WHERE Airport_Name = %s", (Source_airport,))
    source_airport_id = mycursor.fetchone()
    # Get destination airport id from airport table
    mycursor.execute("SELECT Airport_ID FROM airport WHERE Airport_Name = %s", (Destination_airport,))
    destination_airport_id = mycursor.fetchone()

    print(source_airport_id)
    print(destination_airport_id)
    # Enter trip details in trip table
    str = """insert into trip(Flight_ID,src_ID,dest_ID,Depart_time,Arrival_time,first_price,business_price,economy_price) values({},'{}','{}','{}','{}',{},{},{})""".format(
        Flight_ID, source_airport_id, destination_airport_id, Departure, Arrival, First_Class_Price, Business_Class_Price,
        Economy_Class_Price)
    mycursor.execute(str)

    return render(request,'glideEz/Airline_AddTrip.html')


def airline_pricing_view(request):
    return render(request,'glideEz/airline_pricing.html')


def airline_contact_view(request):
    return render(request,'glideEz/airline_contact.html')







