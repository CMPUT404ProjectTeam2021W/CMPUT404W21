function friendToggle(){
  var elem = document.getElementById("friend-button");
  if (elem.value == null){
    console.log("whyyy");
  }
  if (elem.value=="+ Send friend request"){
    elem.value = "✓ Request sent";
    elem.width -= "15px";
  }
  else
  {
    elem.value = "+ Send friend request";
  }
}
