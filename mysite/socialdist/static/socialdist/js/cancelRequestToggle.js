function cancelRequestToggle(){
  var elem = document.getElementById("cancel-button");
  if (elem.value == null){
    console.log("whyyy");
  }
  if (elem.value=="- Cancel friend request"){
    elem.value = "✓ Cancelled";
    elem.width -= "15px";
  }
  else
  {
    elem.value = "- Cancel friend request";
  }
}
