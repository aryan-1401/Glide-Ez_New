// For index

function searchvalidate() {
  let src = document.forms["searchtrip"]["source"].value;
  let dest = document.forms["searchtrip"]["destination"].value;
  let travel = document.forms["searchtrip"]["date_travel"].value;

  // Get today's date in MM/DD/YYYY format
  var today = new Date();
  var dd = String(today.getDate()).padStart(2, '0');
  var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
  mm + 1;
  var yyyy = today.getFullYear();
  today = mm + '/' + dd + '/' + yyyy;

  if (src == "") {
    alert("Source value must be filled out");
    return false;
  }
  if (dest == "") {
    alert("Destination value must be filled out");
    return false;
  }
  if (travel == "") {
    alert("Date of Travel must be filled out");
    return false;
  }
  if (src == dest) {
    alert("Can't Enter same Source And Destination");
    return false;
  }
  if (travel < today) {
    alert("INVALID DATE");
    return false;
  }
}

// For register

function registerUserValidate() {
  let name = document.forms["register"]["username"].value;
  let email = document.forms["register"]["email"].value;
  let password = document.forms["register"]["pass"].value;
  let dob = document.forms["register"]["dob"].value;
  let address = document.forms["register"]["address"].value;
  let aadhar = document.forms["register"]["aadhar"].value;
  let phone = document.forms["register"]["phone"].value;


  if (name == "") {
    alert("Name must be filled out");
    return false;
  }
  if (email == "") {
    alert("Email must be filled out");
    return false;
  }
  // Check for valid email
  if (email.indexOf("@") == -1 || email.indexOf(".") == -1) {
    alert("Invalid Email");
    return false;
  }
  if (password == "") {
    alert("Password must be filled out");
    return false;
  }
  // Check if password is of length 8
  if (password.length < 8) {
    alert("Password must be of length 8");
    return false;
  }
  if (dob == "") {
    alert("Date of Birth must be filled out");
    return false;
  }
  // Check if age is greater than 12
  var today = new Date();
  var birthDate = new Date(dob);
  var age = today.getFullYear() - birthDate.getFullYear();
  var m = today.getMonth() - birthDate.getMonth();
  if (m < 0 || (m === 0 && today.getDate() < birthDate.getDate())) {
    age--;
  }
  if (age < 12) {
    alert("Age must be greater than 12");
    return false;
  }

  if (address == "") {
    alert("Address must be filled out");
    return false;
  }
  if (aadhar == "") {
    alert("Aadhar must be filled out");
    return false;
  }
  if (aadhar.length != 12) {
    alert("Aadhar number must be 12 digits");
    return false;
  }

  if (phone == "") {
    alert("Phone must be filled out");
    return false;
  }
  if (phone.length != 10) {
    alert("Phone number must be 10 digits");
    return false;
  }


  return true;
}

// For login

function loginUserValidate() {
  console.log("loginvalidate");
  let email = document.forms["login"]["login_email"].value;
  let password = document.forms["login"]["login_password"].value;

  if (email == "") {
    alert("Email must be filled out");
    return false;
  }
  if (password == "") {
    alert("Password must be filled out");
    return false;
  }
  if (email.indexOf("@") == -1 || email.indexOf(".") == -1) {
    alert("Invalid Email");
    return false;
  }
  return true;

}