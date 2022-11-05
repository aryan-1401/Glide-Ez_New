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