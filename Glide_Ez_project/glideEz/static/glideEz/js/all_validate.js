function searchvalidate() {
    let src = document.forms["searchtrip"]["source"].value;
    let dest = document.forms["searchtrip"]["destination"].value;
    let travel = document.forms["searchtrip"]["date_travel"].value;
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
  if (travel < new Date().toISOString().split("T")[0]) {
    alert("INVALID DATE");
    return false;
  }
  }